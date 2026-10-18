from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.db import get_db
from config.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    create_email_verification_token,
    hash_email_verification_token,
)
from models.User import User
from Schemas.User import UserCreate, UsernameUpdate, PasswordChange
from datetime import datetime, timedelta, timezone

from models.EmailVerification import EmailVerification
from config.email import send_email


from pydantic import EmailStr

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_data.username)
        | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        is_verified=False,
    )

    db.add(new_user)
    db.flush()

    token = create_email_verification_token()
    token_hash = hash_email_verification_token(token)

    verification = EmailVerification(
        user_id=new_user.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    )

    db.add(verification)
    db.commit()
    db.refresh(new_user)

    verification_link = (
        f"http://127.0.0.1:8000/auth/verify-email?token={token}"
    )

    try:
        send_email(
            to=new_user.email,
            subject="Acikarttirma - E-poçt təsdiqi",
            html=f"""
                <h2>Salam, {new_user.username}!</h2>
                <p>Hesabını təsdiqləmək üçün aşağıdakı linkə daxil ol:</p>
                <p><a href="{verification_link}">E-poçtumu təsdiqlə</a></p>
                <p>Bu link 30 dəqiqə ərzində etibarlıdır.</p>
            """,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Hesab yaradıldı, lakin təsdiq e-poçtu göndərilmədi. "
                "Yenidən göndərmə funksiyasını növbəti addımda əlavə edəcəyik."
            ),
        )

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "is_verified": new_user.is_verified,
        "message": "Qeydiyyat tamamlandı. E-poçtunu təsdiqlə.",
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Daxil olmaq üçün əvvəlcə e-poçtunu təsdiqlə.",
        )
    
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }


@router.patch("/username")
def update_username(
    data: UsernameUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_username = data.username.strip()

    if len(new_username) < 3:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username must contain at least 3 characters",
        )

    if new_username == current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is already your username",
        )

    existing_user = db.query(User).filter(
        User.username == new_username,
        User.id != current_user.id,
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    now = datetime.now(timezone.utc)
    last_changed = current_user.username_changed_at

    if last_changed is not None:
        if last_changed.tzinfo is None:
            last_changed = last_changed.replace(tzinfo=timezone.utc)

        next_change = last_changed + timedelta(days=30)

        if now < next_change:
            remaining = next_change - now
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "message": "Username can only be changed once every 30 days",
                    "next_change_at": next_change.isoformat(),
                    "remaining_seconds": int(remaining.total_seconds()),
                },
            )

    current_user.username = new_username
    current_user.username_changed_at = now

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Username updated successfully",
        "username": current_user.username,
        "next_change_at": (
            now + timedelta(days=30)
        ).isoformat(),
    }

@router.patch("/password")
def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account does not have a local password",
        )

    if not verify_password(
        data.current_password,
        current_user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    current_user.password_hash = hash_password(data.new_password)

    db.commit()

    return {"message": "Password changed successfully"}


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    token_hash = hash_email_verification_token(token)

    verification = db.query(EmailVerification).filter(
        EmailVerification.token_hash == token_hash
    ).first()

    if verification is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Təsdiq linki yanlışdır və ya artıq istifadə edilib.",
        )

    now = datetime.now(timezone.utc)
    expires_at = verification.expires_at

    # SQLite timezone məlumatını itirə bilər.
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        db.delete(verification)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Təsdiq linkinin vaxtı bitib.",
        )

    user = db.query(User).filter(
        User.id == verification.user_id
    ).first()

    if user is None:
        db.delete(verification)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="İstifadəçi tapılmadı.",
        )

    user.is_verified = True
    db.delete(verification)
    db.commit()

    return {
        "message": "E-poçt uğurla təsdiqləndi. İndi daxil ola bilərsən."
    }


@router.post("/resend-verification")
def resend_verification(
    email: EmailStr,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()

    # E-poçtun sistemdə olub-olmadığını açıqlamırıq.
    if user is None or user.is_verified:
        return {
            "message": (
                "Əgər hesab mövcuddursa və təsdiqlənməyibsə, "
                "təsdiq təlimatları göndəriləcək."
            )
        }

    
    latest_verification = (
        db.query(EmailVerification)
        .filter(EmailVerification.user_id == user.id)
        .order_by(EmailVerification.created_at.desc())
        .first()
    )

    if latest_verification:
        created_at = latest_verification.created_at

        # SQLite tarixi timezone məlumatı olmadan qaytara bilər.
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        elapsed = datetime.now(timezone.utc) - created_at

        if elapsed < timedelta(seconds=60):
            return {
                "message": (
                    "Əgər hesab mövcuddursa və təsdiqlənməyibsə, "
                    "təsdiq təlimatları göndəriləcək."
                )
            }


    # İstifadəçinin əvvəlki təsdiq tokenlərini etibarsızlaşdırırıq.
    db.query(EmailVerification).filter(
        EmailVerification.user_id == user.id
    ).delete(synchronize_session=False)

    token = create_email_verification_token()
    token_hash = hash_email_verification_token(token)

    verification = EmailVerification(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    )

    db.add(verification)
    db.commit()

    verification_link = (
        f"http://127.0.0.1:8000/auth/verify-email?token={token}"
    )

    try:
        send_email(
            to=user.email,
            subject="Acikarttirma - E-poçt təsdiqi",
            html=f"""
                <h2>Salam, {user.username}!</h2>
                <p>E-poçtunu təsdiqləmək üçün bu linkə daxil ol:</p>
                <p><a href="{verification_link}">E-poçtumu təsdiqlə</a></p>
                <p>Link 30 dəqiqə ərzində etibarlıdır.</p>
            """,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Təsdiq e-poçtu göndərilə bilmədi.",
        )

    return {
        "message": (
            "Əgər hesab mövcuddursa və təsdiqlənməyibsə, "
            "təsdiq təlimatları göndəriləcək."
        )
    }

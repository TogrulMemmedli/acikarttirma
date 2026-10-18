
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from config.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    username_changed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    google_sub: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True, index=True
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

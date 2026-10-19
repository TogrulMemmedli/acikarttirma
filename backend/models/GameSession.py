
import secrets

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from config.db import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id"),
        nullable=False,
        index=True,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    invite_code: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
        default=lambda: secrets.token_urlsafe(12),
        nullable=False,
    )

    starting_balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    character_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    time_limit_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="waiting",
        nullable=False,
        index=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    started_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    finished_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from config.db import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    last_seen_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

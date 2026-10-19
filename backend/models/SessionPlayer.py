
from sqlalchemy import DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from config.db import Base


class SessionPlayer(Base):
    __tablename__ = "session_players"

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "player_id",
            name="uq_session_player",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("game_sessions.id"),
        nullable=False,
        index=True,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True,
    )

    is_ready: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    joined_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    left_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

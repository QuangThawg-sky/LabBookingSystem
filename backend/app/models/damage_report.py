
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DamageReport(Base):
    __tablename__ = "damage_reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    loan_id: Mapped[int] = mapped_column(
        ForeignKey("loans.id", ondelete="CASCADE"),
        nullable=False
    )

    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    image_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="reported"
    )

    loan: Mapped[Loan] = relationship(
        "Loan",
        back_populates="damage_reports"
    )

    reporter: Mapped[User] = relationship(
        "User",
        back_populates="damage_reports"
    )

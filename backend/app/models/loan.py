
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    booking_equipment_id: Mapped[int] = mapped_column(
        ForeignKey("booking_equipment.id", ondelete="CASCADE"),
        nullable=False
    )

    checkout_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    return_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    condition_on_return: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="borrowed"
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    booking_equipment: Mapped[BookingEquipment] = relationship(
        "BookingEquipment",
        back_populates="loans"
    )

    damage_reports: Mapped[list[DamageReport]] = relationship(
        "DamageReport",
        back_populates="loan",
        cascade="all, delete-orphan"
    )

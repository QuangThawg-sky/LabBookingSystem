
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BookingEquipment(Base):
    __tablename__ = "booking_equipment"

    __table_args__ = (
        UniqueConstraint(
            "booking_id",
            "equipment_id",
            name="uq_booking_equipment"
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_booking_equipment_quantity"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False
    )

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    booking: Mapped[Booking] = relationship(
        "Booking",
        back_populates="booking_equipment"
    )

    equipment: Mapped[Equipment] = relationship(
        "Equipment",
        back_populates="booking_equipment"
    )

    loans: Mapped[list[Loan]] = relationship(
        "Loan",
        back_populates="booking_equipment",
        cascade="all, delete-orphan"
    )


from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    CheckConstraint,
    Index,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        CheckConstraint(
            "end_time > start_time",
            name="ck_booking_valid_time"
        ),
        Index("ix_booking_room_time", "room_id", "start_time", "end_time"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
        nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    purpose: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="bookings"
    )

    room: Mapped[Room] = relationship(
        "Room",
        back_populates="bookings"
    )

    booking_equipment: Mapped[list[BookingEquipment]] = relationship(
        "BookingEquipment",
        back_populates="booking",
        cascade="all, delete-orphan"
    )

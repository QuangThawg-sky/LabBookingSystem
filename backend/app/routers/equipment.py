
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Equipment
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
)
from app.security.dependencies import get_current_user, require_roles


router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.get("/", response_model=list[EquipmentResponse])
def get_equipment(
    search: str | None = Query(default=None, max_length=150),
    status: str | None = Query(
        default=None,
        pattern="^(available|in_use|maintenance|damaged)$"
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = select(Equipment)

    if search:
        query = query.where(
            Equipment.name.ilike(f"%{search}%")
            | Equipment.asset_code.ilike(f"%{search}%")
        )

    if status:
        query = query.where(Equipment.status == status)

    query = query.order_by(Equipment.id).offset(skip).limit(limit)

    return db.scalars(query).all()


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment_detail(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    equipment = db.get(Equipment, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy thiết bị"
        )

    return equipment


@router.post("/", response_model=EquipmentResponse, status_code=201)
def create_equipment(
    request: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("staff")),
):
    equipment = Equipment(**request.model_dump())
    db.add(equipment)

    try:
        db.commit()
        db.refresh(equipment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Mã tài sản đã tồn tại"
        )

    return equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    request: EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("staff")),
):
    equipment = db.get(Equipment, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy thiết bị"
        )

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(equipment, key, value)

    try:
        db.commit()
        db.refresh(equipment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Mã tài sản đã tồn tại"
        )

    return equipment


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("staff")),
):
    equipment = db.get(Equipment, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy thiết bị"
        )

    if equipment.booking_equipment:
        raise HTTPException(
            status_code=409,
            detail="Không thể xóa thiết bị đã được sử dụng trong đặt lịch"
        )

    db.delete(equipment)
    db.commit()

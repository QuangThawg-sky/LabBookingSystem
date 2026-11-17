
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Room
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.security.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomResponse])
def get_rooms(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.scalars(select(Room).order_by(Room.id)).all()


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    room = db.get(Room, room_id)

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng thực hành"
        )

    return room


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED
)
def create_room(
    request: RoomCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("staff"))
):
    room = Room(**request.model_dump())
    db.add(room)

    try:
        db.commit()
        db.refresh(room)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tên phòng đã tồn tại"
        )

    return room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    request: RoomUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("staff"))
):
    room = db.get(Room, room_id)

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng thực hành"
        )

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)

    try:
        db.commit()
        db.refresh(room)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tên phòng đã tồn tại"
        )

    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("staff"))
):
    room = db.get(Room, room_id)

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng thực hành"
        )

    db.delete(room)
    db.commit()

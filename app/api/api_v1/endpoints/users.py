from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_welcome_email

router = APIRouter()


@router.get("/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Read users
    """
    users = crud.user.read_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create user
    """
    user = crud.user.read_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario con este correo ya existe en el sistema",
        )
    user = crud.user.create(db, obj_in=user_in)
    send_welcome_email(email_to=user_in.email, full_name=user_in.full_name)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Read current user
    """
    return current_user


@router.patch("/me", response_model=schemas.User)
def update_user_me(
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update current user
    """
    user_in = user_in.copy(update={"is_superuser": False})
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create user without the need to be logged in
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El registro abierto de usuarios está prohibido en este servidor",
        )
    user = crud.user.read_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario con este correo ya existe en el sistema",
        )
    user_in = user_in.copy(update={"is_active": True, "is_superuser": False})
    user = crud.user.create(db, obj_in=user_in)
    send_welcome_email(email_to=user_in.email, full_name=user_in.full_name)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Read user
    """
    user = crud.user.read(db, id=user_id)
    return user


@router.patch("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update user
    """
    user = crud.user.read(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario con este correo no existe en el sistema",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

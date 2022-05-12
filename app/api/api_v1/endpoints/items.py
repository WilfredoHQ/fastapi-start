from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Read items
    """
    items = crud.item.read_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create item
    """
    item = crud.item.create_with_owner(db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(
    item_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Read item
    """
    item = crud.item.read(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado"
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay suficientes permisos",
        )
    return item


@router.delete("/{item_id}", response_model=schemas.Item)
def delete_item(
    item_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Delete item
    """
    item = crud.item.read(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado"
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay suficientes permisos",
        )
    item = crud.item.delete(db, db_obj=item)
    return item


@router.patch("/{item_id}", response_model=schemas.Item)
def update_item(
    item_id: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update item
    """
    item = crud.item.read(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado"
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay suficientes permisos",
        )
    item = crud.item.update(db, db_obj=item, obj_in=item_in)
    return item

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        db_obj = Item(**obj_in.dict(), owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[Item]:
        return (
            db.query(Item)
            .filter(Item.owner_id == owner_id)
            .order_by(Item.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


item = CRUDItem(Item)

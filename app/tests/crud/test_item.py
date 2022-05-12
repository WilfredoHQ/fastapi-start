from sqlalchemy.orm import Session

from app import crud, schemas
from app.tests.utils.item import create_random_item
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create(db: Session) -> None:
    title = random_lower_string()
    item_in = schemas.ItemCreate(title=title)
    item = crud.item.create(db, obj_in=item_in)
    assert item.title == title


def test_create_with_owner(db: Session) -> None:
    user = create_random_user(db)
    title = random_lower_string()
    item_in = schemas.ItemCreate(title=title)
    item = crud.item.create_with_owner(db, obj_in=item_in, owner_id=user.id)
    assert item.title == title


def test_read(db: Session) -> None:
    item = create_random_item(db)
    stored_item = crud.item.read(db, id=item.id)
    assert stored_item
    assert stored_item.title == item.title


def test_read_multi(db: Session) -> None:
    create_random_item(db)
    create_random_item(db)
    stored_items = crud.item.read_multi(db)
    assert len(stored_items) > 1
    for stored_item in stored_items:
        assert hasattr(stored_item, "title")


def test_read_multi_by_owner(db: Session) -> None:
    user = create_random_user(db)
    create_random_item(db, owner_id=user.id)
    create_random_item(db, owner_id=user.id)
    stored_items = crud.item.read_multi_by_owner(db, owner_id=user.id)
    assert len(stored_items) > 1
    for stored_item in stored_items:
        assert hasattr(stored_item, "title")
        assert stored_item.owner_id == user.id


def test_update(db: Session) -> None:
    item = create_random_item(db)
    new_title = random_lower_string()
    item_in_update = schemas.ItemUpdate(title=new_title)
    updated_item = crud.item.update(db, db_obj=item, obj_in=item_in_update)
    assert updated_item.id == item.id
    assert updated_item.title == new_title


def test_delete(db: Session) -> None:
    item = create_random_item(db)
    deleted_item = crud.item.delete(db, db_obj=item)
    ask_item = crud.item.read(db, id=item.id)
    assert ask_item is None
    assert deleted_item.id == item.id
    assert deleted_item.title == item.title

from sqlalchemy.orm import Session

from app import crud, schemas
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


def test_create(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email


def test_read(db: Session) -> None:
    user = create_random_user(db)
    stored_user = crud.user.read(db, id=user.id)
    assert stored_user
    assert stored_user.email == user.email


def test_read_multi(db: Session) -> None:
    create_random_user(db)
    create_random_user(db)
    stored_users = crud.user.read_multi(db)
    assert len(stored_users) > 1
    for stored_user in stored_users:
        assert hasattr(stored_user, "email")


def test_read_by_email(db: Session) -> None:
    user = create_random_user(db)
    stored_user = crud.user.read_by_email(db, email=user.email)
    assert stored_user
    assert stored_user.email == user.email


def test_update(db: Session) -> None:
    user = create_random_user(db)
    new_full_name = random_lower_string()
    user_in_update = schemas.UserUpdate(full_name=new_full_name)
    updated_user = crud.user.update(db, db_obj=user, obj_in=user_in_update)
    assert updated_user.id == user.id
    assert updated_user.full_name == new_full_name
    assert updated_user.email == user.email


def test_delete(db: Session) -> None:
    user = create_random_user(db)
    deleted_user = crud.user.delete(db, db_obj=user)
    ask_user = crud.user.read(db, id=user.id)
    assert ask_user is None
    assert deleted_user.id == user.id
    assert deleted_user.email == user.email


def test_authenticate(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert authenticated_user.email == user.email

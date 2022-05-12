from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


def create_random_user(db: Session) -> models.User:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    return crud.user.create(db, obj_in=user_in)


def create_test_user(db: Session) -> models.User:
    email = settings.EMAIL_TEST_USER
    password = random_lower_string()
    user = crud.user.read_by_email(db, email=email)
    if not user:
        user_in_create = schemas.UserCreate(email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    return user


def user_authentication_headers(
    client: TestClient, email: str, password: str
) -> dict[str, str]:
    login_data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
    db: Session, *, client: TestClient
) -> dict[str, str]:
    """
    Return a valid token for the user with given email

    If the user doesn't exist it is created first
    """
    password = random_lower_string()
    user = create_test_user(db)
    user_in_update = schemas.UserUpdate(password=password)
    user = crud.user.update(db, db_obj=user, obj_in=user_in_update)
    return user_authentication_headers(
        client=client, email=user.email, password=password
    )

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


def test_read_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    create_random_user(db)
    create_random_user(db)
    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert result
    assert len(result) > 1
    for result_user in result:
        assert "email" in result_user


def test_create_user(client: TestClient, superuser_token_headers: dict) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["email"] == email


def test_read_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["email"] == settings.EMAIL_TEST_USER


def test_update_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    new_full_name = random_lower_string()
    data = {"full_name": new_full_name}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers, json=data
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["full_name"] == new_full_name
    assert result["email"] == settings.EMAIL_TEST_USER


def test_create_user_open(client: TestClient) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/users/open", json=data)
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["email"] == email


def test_read_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=superuser_token_headers
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["email"] == user.email


def test_update_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    user = create_random_user(db)
    new_full_name = random_lower_string()
    data = {"full_name": new_full_name}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=superuser_token_headers,
        json=data,
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["full_name"] == new_full_name
    assert result["email"] == user.email

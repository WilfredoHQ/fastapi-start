from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item
from app.tests.utils.user import create_test_user
from app.tests.utils.utils import random_lower_string


def test_read_items(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_test_user(db)
    create_random_item(db, owner_id=user.id)
    create_random_item(db, owner_id=user.id)
    r = client.get(f"{settings.API_V1_STR}/items/", headers=normal_user_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert result
    assert len(result) > 1
    for result_item in result:
        assert "title" in result_item
        assert result_item["owner_id"] == user.id


def test_create_item(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_test_user(db)
    title = random_lower_string()
    data = {"title": title}
    r = client.post(
        f"{settings.API_V1_STR}/items/", headers=normal_user_token_headers, json=data
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["title"] == title
    assert result["owner_id"] == user.id


def test_read_item(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_test_user(db)
    item = create_random_item(db, owner_id=user.id)
    r = client.get(
        f"{settings.API_V1_STR}/items/{item.id}", headers=normal_user_token_headers
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["title"] == item.title
    assert result["owner_id"] == user.id


def test_delete_item(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_test_user(db)
    item = create_random_item(db, owner_id=user.id)
    r = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}", headers=normal_user_token_headers
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["title"] == item.title
    assert result["owner_id"] == user.id


def test_update_item(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_test_user(db)
    item = create_random_item(db, owner_id=user.id)
    new_title = random_lower_string()
    data = {"title": new_title}
    r = client.patch(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert result["title"] == new_title
    assert result["owner_id"] == user.id

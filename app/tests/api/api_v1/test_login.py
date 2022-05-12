from fastapi.testclient import TestClient

from app.core.config import settings


def test_login_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    result = r.json()
    assert r.status_code == 200
    assert result
    assert "access_token" in result


def test_test_token(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token", headers=normal_user_token_headers
    )
    result = r.json()
    assert r.status_code == 200
    assert result
    assert "email" in result

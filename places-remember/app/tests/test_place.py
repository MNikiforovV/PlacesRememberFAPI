import pytest
from ..main import app
from ..dependencies import get_user


def test_read_add_place_unauthorized(client):
    response = client.get("/place/add-place")
    assert response.status_code == 403


user_dependencie = (
            app,
            {get_user: lambda: {"id": 1, "email": "test@test.com"}},
        )


@pytest.mark.parametrize(
    "fastapi_dep",
    [user_dependencie],
    indirect=True,
)
def test_read_add_place_authorized(client, fastapi_dep):
    response = client.get("/place/add-place")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "fastapi_dep",
    [user_dependencie],
    indirect=True,
)
def test_create_place_authorized(client, fastapi_dep):
    response = client.post(
        url="/place/add-place",
        data={
            "title": "foo",
            "description": "bar",
            "latitude": 0,
            "longitude": 0,
        }
    )
    assert response.status_code == 200

    response = client.get("/place/get-place/1")
    assert response.status_code == 200

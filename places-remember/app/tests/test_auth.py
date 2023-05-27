


def test_read_main_authorized(client):

    response = client.get("/", cookies={})
    assert response == 200

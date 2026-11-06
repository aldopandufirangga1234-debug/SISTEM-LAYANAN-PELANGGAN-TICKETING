from app import create_app


def test_app_loads():
    app = create_app()
    client = app.test_client()
    response = client.get('/')
    assert response.status_code in (200, 302)

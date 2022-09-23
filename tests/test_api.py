import pytest
from checkoutbot.api import app
from flask.testing import FlaskClient

API_HOME = "http://localhost:5000"


@pytest.fixture()
def app():
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health(client: FlaskClient):
    # api response
    response = client.get(f"{API_HOME}/health")

    # validation
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "OK"

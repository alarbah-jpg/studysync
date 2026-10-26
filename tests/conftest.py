import pytest

from app import create_app, db
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, name="Alice", email="alice@example.com", password="password123"):
    return client.post("/register", data={"name": name, "email": email, "password": password},
                       follow_redirects=True)


def login(client, email="alice@example.com", password="password123"):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


def logout(client):
    return client.post("/logout", follow_redirects=True)


def create_group(client, name="Algorithms Group"):
    client.post("/groups/create", data={"name": name}, follow_redirects=True)
    from app.models import Group
    return Group.query.filter_by(name=name).first()

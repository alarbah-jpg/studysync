from app.models import User
from tests.conftest import login, logout, register


def test_register_creates_hashed_user(client):
    r = register(client)
    assert b"Welcome to StudySync" in r.data
    user = User.query.filter_by(email="alice@example.com").first()
    assert user is not None and user.password_hash != "password123"  # FR1, FR2


def test_duplicate_email_rejected(client):
    register(client)
    logout(client)
    r = register(client, name="Other")
    assert b"already registered" in r.data
    assert User.query.count() == 1


def test_short_password_rejected(client):
    r = register(client, password="short")
    assert b"at least 8 characters" in r.data
    assert User.query.count() == 0


def test_login_logout(client):
    register(client)
    logout(client)
    assert b"My study groups" in login(client).data
    assert b"Log in" in logout(client).data


def test_wrong_password(client):
    register(client)
    logout(client)
    assert b"Invalid email or password" in login(client, password="wrongpass1").data


def test_protected_page_redirects_to_login(client):
    r = client.get("/")
    assert r.status_code == 302 and "/login" in r.headers["Location"]

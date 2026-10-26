from app import db
from app.models import Group, Membership
from tests.conftest import create_group, logout, register


def test_creator_becomes_admin(client):
    register(client)
    g = create_group(client)
    m = Membership.query.filter_by(group_id=g.id).first()
    assert m.role == "admin" and len(g.join_code) == 6  # FR3, FR4


def test_join_with_valid_and_invalid_code(client):
    register(client)
    g = create_group(client)
    logout(client)
    register(client, name="Bob", email="bob@example.com")
    assert b"Invalid join code" in client.post("/groups/join", data={"code": "ZZZZZZ"}, follow_redirects=True).data
    r = client.post("/groups/join", data={"code": g.join_code.lower()}, follow_redirects=True)
    assert b"Joined Algorithms Group" in r.data
    assert Membership.query.filter_by(group_id=g.id).count() == 2


def test_user_can_belong_to_multiple_groups(client):
    register(client)
    create_group(client, "G1")
    create_group(client, "G2")
    r = client.get("/")
    assert b"G1" in r.data and b"G2" in r.data  # FR10


def test_admin_can_delete_group(client):
    register(client)
    g = create_group(client)
    client.post(f"/groups/{g.id}/delete", follow_redirects=True)
    assert db.session.get(Group, g.id) is None

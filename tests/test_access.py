from app.models import Group, Membership, Task
from tests.conftest import create_group, logout, register


def setup_two_users(client):
    register(client)
    g = create_group(client)
    client.post(f"/groups/{g.id}/tasks/new", data={"title": "Secret"})
    logout(client)
    register(client, name="Bob", email="bob@example.com")
    return g


def test_non_member_cannot_view_or_modify(client):
    g = setup_two_users(client)
    t = Task.query.first()
    assert client.get(f"/groups/{g.id}").status_code == 403  # FR9
    assert client.post(f"/groups/{g.id}/tasks/new", data={"title": "x"}).status_code == 403
    assert client.post(f"/tasks/{t.id}/status", data={"status": "Done"}).status_code == 403
    assert client.post(f"/tasks/{t.id}/delete").status_code == 403
    assert Task.query.count() == 1


def test_member_cannot_delete_group_or_remove_members(client):
    g = setup_two_users(client)
    client.post("/groups/join", data={"code": g.join_code})
    assert client.post(f"/groups/{g.id}/delete").status_code == 403
    admin_uid = Membership.query.filter_by(role="admin").first().user_id
    assert client.post(f"/groups/{g.id}/members/{admin_uid}/remove").status_code == 403
    assert Group.query.count() == 1


def test_member_cannot_change_status_of_others_task(client):
    g = setup_two_users(client)
    client.post("/groups/join", data={"code": g.join_code})
    t = Task.query.first()  # unassigned, Bob is plain member
    assert client.post(f"/tasks/{t.id}/status", data={"status": "Done"}).status_code == 403


def test_admin_can_remove_member(client):
    g = setup_two_users(client)
    client.post("/groups/join", data={"code": g.join_code})
    bob_id = Membership.query.filter_by(role="member").first().user_id
    logout(client)
    from tests.conftest import login
    login(client)
    client.post(f"/groups/{g.id}/members/{bob_id}/remove")
    assert Membership.query.filter_by(group_id=g.id).count() == 1


def test_missing_group_is_404(client):
    register(client)
    assert client.get("/groups/999").status_code == 404

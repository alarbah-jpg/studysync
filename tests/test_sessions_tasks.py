from datetime import datetime, timedelta

from app import db
from app.models import StudySession, Task, User
from tests.conftest import create_group, register


def future_str(days=2):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%dT%H:%M")


def test_session_crud(client):
    register(client)
    g = create_group(client)
    client.post(f"/groups/{g.id}/sessions/new", data={
        "title": "Midterm review", "topic": "Graphs", "start_time": future_str(), "location": "Library"})
    s = StudySession.query.first()
    assert s.title == "Midterm review"  # FR5
    assert b"Midterm review" in client.get(f"/groups/{g.id}").data
    client.post(f"/sessions/{s.id}/edit", data={
        "title": "Final review", "topic": "Graphs", "start_time": future_str(3), "location": "Room 5"})
    assert db.session.get(StudySession, s.id).title == "Final review"
    client.post(f"/sessions/{s.id}/delete")
    assert StudySession.query.count() == 0


def test_session_requires_title_and_valid_time(client):
    register(client)
    g = create_group(client)
    r = client.post(f"/groups/{g.id}/sessions/new", data={"title": "", "start_time": "bad"})
    assert b"required" in r.data and StudySession.query.count() == 0


def test_task_create_assign_and_status(client):
    register(client)
    g = create_group(client)
    uid = User.query.first().id
    client.post(f"/groups/{g.id}/tasks/new", data={
        "title": "Write intro", "description": "x", "due_date": "2030-01-01", "assignee_id": uid})
    t = Task.query.first()
    assert t.assignee_id == uid and t.status == "To Do"  # FR6
    for status in ("In Progress", "Done"):
        client.post(f"/tasks/{t.id}/status", data={"status": status})
        assert db.session.get(Task, t.id).status == status  # FR7
    assert client.post(f"/tasks/{t.id}/status", data={"status": "Bogus"}).status_code == 400


def test_dashboard_progress(client):
    register(client)
    g = create_group(client)
    for title in ("a", "b", "c", "d"):
        client.post(f"/groups/{g.id}/tasks/new", data={"title": title})
    done = Task.query.first()
    client.post(f"/tasks/{done.id}/status", data={"status": "Done"})
    assert b"Overall progress: 25%" in client.get(f"/groups/{g.id}").data  # FR8


def test_assignee_must_be_member(client):
    register(client)
    g = create_group(client)
    r = client.post(f"/groups/{g.id}/tasks/new", data={"title": "x", "assignee_id": 999})
    assert b"must be a member" in r.data and Task.query.count() == 0

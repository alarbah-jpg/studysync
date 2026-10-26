"""Create demo data for the final presentation: python seed.py"""
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Group, Membership, StudySession, Task, User

app = create_app()
with app.app_context():
    if User.query.filter_by(email="alice@example.com").first():
        print("Demo data already exists.")
        raise SystemExit
    alice, bob = User(name="Alice", email="alice@example.com"), User(name="Bob", email="bob@example.com")
    alice.set_password("password123")
    bob.set_password("password123")
    g = Group(name="CS 6xx Project Team", join_code="DEMO01")
    db.session.add_all([alice, bob, g])
    db.session.flush()
    db.session.add_all([
        Membership(user_id=alice.id, group_id=g.id, role="admin"),
        Membership(user_id=bob.id, group_id=g.id, role="member"),
        StudySession(group_id=g.id, title="Design review", topic="Architecture",
                     start_time=datetime.now() + timedelta(days=2), location="Library room 3"),
        Task(group_id=g.id, title="Draft requirements", status="Done", assignee_id=alice.id),
        Task(group_id=g.id, title="Write test cases", status="In Progress", assignee_id=bob.id),
        Task(group_id=g.id, title="Prepare demo", status="To Do", assignee_id=alice.id),
    ])
    db.session.commit()
    print("Seeded. Log in as alice@example.com / password123")

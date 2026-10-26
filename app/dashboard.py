from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.helpers import completion_percent, get_group_membership
from app.models import TASK_STATUSES, Membership, StudySession, Task

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    memberships = Membership.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", memberships=memberships)


@bp.route("/groups/<int:group_id>")
@login_required
def group_dashboard(group_id):
    group, me = get_group_membership(group_id)
    upcoming = (StudySession.query.filter_by(group_id=group.id)
                .filter(StudySession.start_time >= datetime.now())
                .order_by(StudySession.start_time).all())
    tasks = Task.query.filter_by(group_id=group.id).order_by(Task.due_date).all()
    by_status = {s: [t for t in tasks if t.status == s] for s in TASK_STATUSES}
    return render_template("group_dashboard.html", group=group, me=me, upcoming=upcoming,
                           by_status=by_status, statuses=TASK_STATUSES,
                           percent=completion_percent(tasks), total=len(tasks))

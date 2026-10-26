from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.helpers import get_group_membership, parse_date
from app.models import TASK_STATUSES, Membership, Task

bp = Blueprint("tasks", __name__)


def _fill(task, form, group_id):
    title = form.get("title", "").strip()
    if not title:
        flash("Task title is required.", "danger")
        return False
    assignee_id = form.get("assignee_id", type=int)
    if assignee_id and not Membership.query.filter_by(group_id=group_id, user_id=assignee_id).first():
        flash("Assignee must be a member of the group.", "danger")
        return False
    task.title = title
    task.description = form.get("description", "").strip()
    task.due_date = parse_date(form.get("due_date"))
    task.assignee_id = assignee_id or None
    return True


@bp.route("/groups/<int:group_id>/tasks/new", methods=["GET", "POST"])
@login_required
def create(group_id):
    group, _ = get_group_membership(group_id)
    if request.method == "POST":
        t = Task(group_id=group.id, status="To Do")
        if _fill(t, request.form, group.id):
            db.session.add(t)
            db.session.commit()
            flash("Task created.", "success")
            return redirect(url_for("dashboard.group_dashboard", group_id=group.id))
    return render_template("task_form.html", group=group, task=None)


@bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit(task_id):
    t = db.get_or_404(Task, task_id)
    group, _ = get_group_membership(t.group_id)
    if request.method == "POST" and _fill(t, request.form, group.id):
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("dashboard.group_dashboard", group_id=group.id))
    return render_template("task_form.html", group=group, task=t)


@bp.route("/tasks/<int:task_id>/status", methods=["POST"])
@login_required
def set_status(task_id):
    t = db.get_or_404(Task, task_id)
    _, me = get_group_membership(t.group_id)
    if not (me.is_admin or t.assignee_id == current_user.id):
        abort(403)  # FR7: only assignee or admin
    status = request.form.get("status")
    if status not in TASK_STATUSES:
        abort(400)
    t.status = status
    db.session.commit()
    return redirect(url_for("dashboard.group_dashboard", group_id=t.group_id))


@bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete(task_id):
    t = db.get_or_404(Task, task_id)
    get_group_membership(t.group_id)
    gid = t.group_id
    db.session.delete(t)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("dashboard.group_dashboard", group_id=gid))

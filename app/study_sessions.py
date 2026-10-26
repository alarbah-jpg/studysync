from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.helpers import get_group_membership, parse_datetime
from app.models import StudySession

bp = Blueprint("study_sessions", __name__)


def _fill(session, form):
    title = form.get("title", "").strip()
    start = parse_datetime(form.get("start_time"))
    if not title or start is None:
        flash("Title and a valid date/time are required.", "danger")
        return False
    session.title = title
    session.topic = form.get("topic", "").strip()
    session.start_time = start
    session.location = form.get("location", "").strip()
    return True


@bp.route("/groups/<int:group_id>/sessions/new", methods=["GET", "POST"])
@login_required
def create(group_id):
    group, _ = get_group_membership(group_id)
    if request.method == "POST":
        s = StudySession(group_id=group.id)
        if _fill(s, request.form):
            db.session.add(s)
            db.session.commit()
            flash("Session scheduled.", "success")
            return redirect(url_for("dashboard.group_dashboard", group_id=group.id))
    return render_template("session_form.html", group=group, session=None)


@bp.route("/sessions/<int:session_id>/edit", methods=["GET", "POST"])
@login_required
def edit(session_id):
    s = db.get_or_404(StudySession, session_id)
    group, _ = get_group_membership(s.group_id)
    if request.method == "POST" and _fill(s, request.form):
        db.session.commit()
        flash("Session updated.", "success")
        return redirect(url_for("dashboard.group_dashboard", group_id=group.id))
    return render_template("session_form.html", group=group, session=s)


@bp.route("/sessions/<int:session_id>/delete", methods=["POST"])
@login_required
def delete(session_id):
    s = db.get_or_404(StudySession, session_id)
    get_group_membership(s.group_id)
    gid = s.group_id
    db.session.delete(s)
    db.session.commit()
    flash("Session deleted.", "success")
    return redirect(url_for("dashboard.group_dashboard", group_id=gid))

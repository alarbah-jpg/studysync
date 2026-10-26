from datetime import date, datetime

from flask import abort
from flask_login import current_user

from app import db
from app.models import Group, Membership


def get_group_membership(group_id):
    """Return (group, membership) or abort: 404 if no group, 403 if not a member (M7 / FR9)."""
    group = db.session.get(Group, group_id)
    if group is None:
        abort(404)
    membership = Membership.query.filter_by(group_id=group_id, user_id=current_user.id).first()
    if membership is None:
        abort(403)
    return group, membership


def require_admin(membership):
    if not membership.is_admin:
        abort(403)


def parse_datetime(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M")
    except (ValueError, TypeError):
        return None


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def completion_percent(tasks):
    if not tasks:
        return 0
    done = sum(1 for t in tasks if t.status == "Done")
    return round(100 * done / len(tasks))

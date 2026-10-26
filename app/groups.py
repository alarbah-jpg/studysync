from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.helpers import get_group_membership, require_admin
from app.models import Group, Membership

bp = Blueprint("groups", __name__, url_prefix="/groups")


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Group name is required.", "danger")
        else:
            group = Group(name=name, join_code=Group.new_join_code())
            db.session.add(group)
            db.session.flush()
            db.session.add(Membership(user_id=current_user.id, group_id=group.id, role="admin"))
            db.session.commit()
            flash(f"Group created. Share join code {group.join_code}.", "success")
            return redirect(url_for("dashboard.group_dashboard", group_id=group.id))
    return render_template("group_form.html", mode="create")


@bp.route("/join", methods=["GET", "POST"])
@login_required
def join():
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        group = Group.query.filter_by(join_code=code).first()
        if group is None:
            flash("Invalid join code.", "danger")
        elif Membership.query.filter_by(group_id=group.id, user_id=current_user.id).first():
            flash("You are already in that group.", "info")
            return redirect(url_for("dashboard.group_dashboard", group_id=group.id))
        else:
            db.session.add(Membership(user_id=current_user.id, group_id=group.id, role="member"))
            db.session.commit()
            flash(f"Joined {group.name}.", "success")
            return redirect(url_for("dashboard.group_dashboard", group_id=group.id))
    return render_template("group_form.html", mode="join")


@bp.route("/<int:group_id>/members/<int:user_id>/remove", methods=["POST"])
@login_required
def remove_member(group_id, user_id):
    group, me = get_group_membership(group_id)
    require_admin(me)
    target = Membership.query.filter_by(group_id=group_id, user_id=user_id).first_or_404()
    if target.user_id == current_user.id:
        flash("Admins cannot remove themselves. Delete the group instead.", "danger")
    else:
        for task in group.tasks:
            if task.assignee_id == user_id:
                task.assignee_id = None
        db.session.delete(target)
        db.session.commit()
        flash("Member removed.", "success")
    return redirect(url_for("dashboard.group_dashboard", group_id=group_id))


@bp.route("/<int:group_id>/delete", methods=["POST"])
@login_required
def delete(group_id):
    group, me = get_group_membership(group_id)
    require_admin(me)
    db.session.delete(group)
    db.session.commit()
    flash("Group deleted.", "success")
    return redirect(url_for("dashboard.index"))

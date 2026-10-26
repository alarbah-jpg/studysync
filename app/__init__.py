from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401
    from app.auth import bp as auth_bp
    from app.groups import bp as groups_bp
    from app.study_sessions import bp as sessions_bp
    from app.tasks import bp as tasks_bp
    from app.dashboard import bp as dashboard_bp

    for bp in (auth_bp, groups_bp, sessions_bp, tasks_bp, dashboard_bp):
        app.register_blueprint(bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403, message="You do not have access to this page."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Page not found."), 404

    with app.app_context():
        db.create_all()

    return app

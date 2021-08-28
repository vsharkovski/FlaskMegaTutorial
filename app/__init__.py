import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import Config, instance_path


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "main.login"
login.login_message = "Please log in to access this page."
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__, instance_path=instance_path)
    app.config.from_object(config_class)

    # create instance folder if needed
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize components, extensions, etc
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # register blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # debugging and logging handlers
    if not app.debug and not app.testing:
        # Configure so errors are sent to admin emails
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr="no-reply@" + app.config["MAIL_SERVER"],
                toaddrs=app.config["ADMINS"], subject="Microblog Failure",
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR) # only send errors
            app.logger.addHandler(mail_handler)

        # Logging to a file
        logs_path = os.path.join(app.instance_path, "logs")
        try:
            os.mkdir(logs_path)
        except OSError:
            pass
        
        file_handler = RotatingFileHandler(
            os.path.join(logs_path, "microblog.log"),
            maxBytes=10240,
            backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname):s %(message)s [in %(pathname):s%(lineno)d]"))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Microblog startup")

    return app


from app import models

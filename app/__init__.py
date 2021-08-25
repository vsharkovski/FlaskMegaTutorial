from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


app = Flask(__name__)

# import config
from config import Config
app.config.from_object(Config)

# create instance folder if needed
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

print(app.config["SQLALCHEMY_DATABASE_URI"])

# database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# users
login = LoginManager(app)
login.login_view = "login"

# debugging and logging
if not app.debug:
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
            secure=secure)
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
        maxBytes=10420,
        backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname):s %(message)s [in %(pathname):s%(lineno)d]"))
    file_handler.setLevel(logging.INFO) # send most things
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)

    # Every time the server is started we log the following
    app.logger.info("Microblog startup")

# import everything else
from app import routes, models, errors

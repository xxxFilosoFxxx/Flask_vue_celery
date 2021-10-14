import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from celery import Celery


app = Flask(__name__, static_url_path='/', static_folder='../dist', template_folder='../dist')
app.config.from_object(os.environ['APP_SETTINGS'])

log_handler = RotatingFileHandler(app.config['LOG_PATH'], maxBytes=10 * 1024 * 1024, backupCount=3)
log_handler.setLevel(logging.ERROR)
app.logger.addHandler(log_handler)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = '/login'

celery = Celery(app.name,
                broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['RESULT_BACKEND'])
celery.conf.update(app.config)

from backend.api import api_bp
app.register_blueprint(api_bp)

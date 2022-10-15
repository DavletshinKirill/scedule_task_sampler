from flask import Flask
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler
from config import config


bootstrap = Bootstrap()
mail = Mail()
schedule = APScheduler()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    schedule.init_app(app)
    from .tasks import send_mail_by_timer
    schedule.add_job(id='1', func=send_mail_by_timer, trigger='interval', seconds=5)
    schedule.start()
    from .send_message import email
    app.register_blueprint(email)
    return app
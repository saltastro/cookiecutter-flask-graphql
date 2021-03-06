"""Top-level package for {{ cookiecutter.project_name }}."""

__author__ = """{{ cookiecutter.full_name }}"""
__version__ = '{{ cookiecutter.version }}'

{% if cookiecutter.log_to_file == "yes" %}import logging
from logging.handlers import RotatingFileHandler
{% endif %}from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy{% if cookiecutter.use_sentry == "yes" %}
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration{% endif %}
from config import config


def log_exception(e):
    """
    Log an exception to Flask's logger{% if cookiecutter.use_sentry == "yes" %} and Sentry{% endif %}.

    Parameters
    ----------
    e : Exception
        The exception to log.

    """

    current_app.logger.exception(e){% if cookiecutter.use_sentry == "yes" %}
    sentry_sdk.capture_exception(e){% endif %}


db = SQLAlchemy()

# these imports can only happen here as otherwise there might be import errors
from app.auth import verify_token  # noqa E402
from app.main import main  # noqa E402
from app.graphql import graphql  # noqa E402

def create_app(config_name):
    app = Flask('__name__')
    app.config.from_object(config[config_name])

    db.init_app(app){% if cookiecutter.log_to_file == "yes" %}

    # logging to file
    log_file_path = app.config['LOG_FILE_PATH']
    if not log_file_path:
        raise Exception('The environment variable LOG_FILE_PATH is not defined')
    handler = RotatingFileHandler(log_file_path,
                                  maxBytes={{ cookiecutter.log_file_max_bytes }},
                                  backupCount={{ cookiecutter.log_file_backup_count }})
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %('
                                  'message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler){% endif %}{% if cookiecutter.use_sentry == "yes" %}

    # setting up Sentry
    sentry_dsn = app.config['SENTRY_DSN']
    if not sentry_dsn:
        app.logger.info('No value is defined for SENTRY_DSN. Have you defined an '
                        'environment variable with this name?')
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FlaskIntegration()]
    ){% endif %}

    app.register_blueprint(graphql)
    app.register_blueprint(main)

    app.before_request(verify_token)

    return app

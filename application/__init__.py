from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy.engine import Engine
from sqlalchemy import event


# This is required for the foreign key constraints and cascading deletes to work properly
# See https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#sqlite-foreign-keys
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


db = SQLAlchemy()


def create_app(test_config=None):
    # Initialize the core application
    app = Flask(__name__)

    # Import the configuration settings from the config file
    app.config.from_pyfile('config.py')
    # Override/update any settings passed into the function
    if test_config is not None:
        app.config.update(test_config)

    # Import the database and marshmallow objects, and attach them to the core application
    from application.models import db, ma
    db.init_app(app)
    ma.init_app(app)

    # Import the Flask blueprints from routes, and register them with the core application
    from application.routes import users_blueprint, questions_blueprint, answers_blueprint, bmuqs_blueprint, bmuas_blueprint
    app.register_blueprint(routes.users_blueprint)
    app.register_blueprint(routes.questions_blueprint)
    app.register_blueprint(routes.answers_blueprint)
    app.register_blueprint(routes.bmuqs_blueprint)
    app.register_blueprint(routes.bmuas_blueprint)

    # Register the error handler functions defined below
    app.register_error_handler(400, handle_errors)
    app.register_error_handler(404, handle_errors)
    app.register_error_handler(409, handle_errors)
    app.register_error_handler(500, handle_errors)
    app.register_error_handler(Exception, handle_generic_exception)

    return app


# Exception handling
def handle_errors(error):
    return make_response(jsonify({'code': error.code, 'message': error.description}), error.code)


def handle_generic_exception(error):
    print(error)
    print(error.args)
    message = "The server encountered an internal error and was unable to complete your request."
    return make_response(jsonify({'code': 500, 'message': message}), 500)
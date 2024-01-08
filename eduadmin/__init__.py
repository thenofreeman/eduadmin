import os

from flask import Flask

KEY='dev'
DB_NAME='eduadmin.sql'

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=KEY,
        DATABASE=os.path.join(app.instance_path, DB_NAME)
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.get('/')
    def index():
        return 'Hello'

    from . import auth, db
    db.init_app(app)
    app.register_blueprint(auth.bp)

    return app
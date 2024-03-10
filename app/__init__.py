from flask import Flask, send_from_directory

from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.hotsauces import bp as hotsauce_bp
    app.register_blueprint(hotsauce_bp, url_prefix='/hotsauces')

    # Configure the static directory
    app.static_folder = 'static'

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        print('AM HERE')
        return send_from_directory(app.static_folder, filename)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
        # Function to create database tables

    def create_db():
        with app.app_context():
            db.create_all()

        # Create database tables when the application starts

    create_db()

    return app

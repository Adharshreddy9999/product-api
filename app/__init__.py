from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from .error_handlers import setup_logging, register_error_handlers
from .config import Config
import logging
from logging.handlers import RotatingFileHandler

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure the Flask application
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:979797@localhost:5432/product_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    with app.app_context():
        # Import parts of our application
        from .models import Product
        from .routes import main, api
        
        # Create database tables
        db.create_all()
        
        # Register blueprints
        app.register_blueprint(main)
        app.register_blueprint(api, url_prefix='/api')  # All API routes will be prefixed with /api
        
        app.logger.info('Application started successfully')
        
        # Configure logging
        if not app.debug:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Application startup')

        # Print URL map for debugging
        print("\nRegistered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")

    return app

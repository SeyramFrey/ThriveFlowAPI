from flask import Flask
from flask_migrate import Migrate
from config import config
from models import db
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    from routes import auth_bp, project_bp, task_bp, expense_bp, suggestion_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(expense_bp, url_prefix='/api/expenses')
    app.register_blueprint(suggestion_bp, url_prefix='/api/suggestions')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 
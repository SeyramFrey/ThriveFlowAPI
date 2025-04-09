from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from .config import Config
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Chargement des variables d'environnement
load_dotenv()

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app, origins="*", supports_credentials=True)
    
    # Configuration
    app.config.from_object(Config)
    
    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Import des modèles pour les migrations
    from app.models.user import User
    from app.models.idea import Idea
    from app.models.project import Project
    
    # Importation des blueprints
    from app.routes.auth import auth_bp
    from app.routes.project_generation import project_gen_bp
    from app.routes.projects import projects_bp
    from app.routes.activities import activities_bp
    
    # Enregistrement des blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(project_gen_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(activities_bp, url_prefix='/api')
    
    # Créer les tables si elles n'existent pas
    with app.app_context():
        db.create_all()
    
    return app 
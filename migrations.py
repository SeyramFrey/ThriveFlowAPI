from flask_migrate import Migrate, upgrade
from app import create_app, db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_migrations():
    app = create_app()
    migrate = Migrate(app, db)
    
    with app.app_context():
        try:
            # Créer les tables et effectuer les migrations
            logger.info("Application des migrations...")
            upgrade()
            
            logger.info("Migrations appliquées avec succès !")
            
        except Exception as e:
            logger.error(f"Erreur lors des migrations : {str(e)}")
            raise

if __name__ == '__main__':
    init_migrations() 
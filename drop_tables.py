from app import create_app
from app.models import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def drop_tables():
    app = create_app()
    with app.app_context():
        try:
            # Supprimer toutes les tables
            logger.info("Suppression de toutes les tables...")
            db.drop_all()
            logger.info("Toutes les tables ont été supprimées avec succès !")
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des tables : {str(e)}")
            raise

if __name__ == '__main__':
    drop_tables() 
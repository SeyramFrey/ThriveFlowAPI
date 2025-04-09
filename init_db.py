from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from app.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    # Créer la base de données si elle n'existe pas
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"Base de données créée : {engine.url}")
    
    # Créer les tables
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    # Supprimer toutes les tables existantes
    metadata.drop_all(bind=engine)
    logger.info("Tables existantes supprimées.")
    
    # Créer toutes les tables
    from app.models.user import User
    from app.models.project import Project, Category, Tag
    from app.models.activity import Activity
    from app.models.idea import Idea
    from app.models.task import Task
    from app.models.resources import TimeTracking, ResourceAllocation
    
    metadata.create_all(bind=engine)
    logger.info("Nouvelles tables créées avec succès !")

if __name__ == '__main__':
    init_db() 
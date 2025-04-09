from app import create_app, db
from flask_migrate import Migrate
import logging
from datetime import datetime
from sqlalchemy.sql import text
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialiser l'application et la base de données
app = create_app()
migrate = Migrate(app, db)

def recreate_tables():
    with app.app_context():
        logging.info("Suppression des tables existantes...")
        db.drop_all()
        logging.info("Tables supprimées.")
        
        logging.info("Création des nouvelles tables...")
        # Création des tables
        db.create_all()
        logging.info("Tables créées avec succès.")
        
        # Création des tables de citation_motivation
        db.session.execute(text("""
        CREATE TABLE IF NOT EXISTS citation_motivation (
            id SERIAL PRIMARY KEY,
            texte TEXT NOT NULL,
            auteur VARCHAR(100),
            categorie VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        
        logging.info("Table citation_motivation créée.")
        
        # Ajouter quelques citations de motivation
        citations = [
            {"texte": "Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte.", "auteur": "Winston Churchill", "categorie": "persévérance"},
            {"texte": "La meilleure façon de prédire l'avenir est de le créer.", "auteur": "Peter Drucker", "categorie": "innovation"},
            {"texte": "Si vous voulez quelque chose que vous n'avez jamais eu, vous devez faire quelque chose que vous n'avez jamais fait.", "auteur": "Thomas Jefferson", "categorie": "changement"},
            {"texte": "Le succès, c'est d'aller d'échec en échec sans perdre son enthousiasme.", "auteur": "Winston Churchill", "categorie": "persévérance"},
            {"texte": "Votre temps est limité, alors ne le gaspillez pas en menant une existence qui n'est pas la vôtre.", "auteur": "Steve Jobs", "categorie": "authenticité"}
        ]
        
        for citation in citations:
            db.session.execute(text(
                "INSERT INTO citation_motivation (texte, auteur, categorie) VALUES (:texte, :auteur, :categorie)"
            ), citation)
        
        db.session.commit()
        logging.info("Citations de motivation ajoutées.")
        
        logging.info("Base de données recréée avec succès.")

if __name__ == "__main__":
    recreate_tables() 
from app import create_app
import logging
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        logging.FileHandler('flask.log'),
        logging.StreamHandler()
    ]
)

# Création de l'application
app = create_app()

if __name__ == '__main__':
    # Configuration du serveur
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    # Démarrage du serveur
    app.run(host=host, port=port, debug=debug) 
import requests
import json
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:5000"
REGISTER_URL = f"{BASE_URL}/api/auth/register"

# Données de test
test_users = [
    {
        "username": "test1",
        "email": "test1@example.com",
        "password": "password123"
    },
    {
        "username": "test2",
        "email": "test2@example.com",
        "password": "password123"
    }
]

def register_test_users():
    for user in test_users:
        logger.info(f"\nEnregistrement de l'utilisateur: {user['username']}")
        
        # Enregistrement de l'utilisateur
        register_response = requests.post(REGISTER_URL, json=user)
        
        if register_response.status_code == 201:
            logger.info(f"Utilisateur {user['username']} créé avec succès")
        else:
            logger.error(f"Échec de l'enregistrement: {register_response.text}")

if __name__ == "__main__":
    register_test_users() 
import requests
import json

# URL de l'API
BASE_URL = "http://127.0.0.1:5000"

# Données d'authentification
auth_data = {
    "username": "testuser",
    "password": "test123"
}

# Authentification
auth_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json=auth_data
)

if auth_response.status_code != 200:
    print("Erreur d'authentification:", auth_response.text)
    exit(1)

# Extraction du token
token = auth_response.json()['access_token']
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Données de test
idea = "Je veux créer une application mobile de gestion de tâches avec des fonctionnalités de collaboration"

# Envoi de la requête
response = requests.post(
    f"{BASE_URL}/api/generate-project",
    headers=headers,
    json={"idea": idea}
)

# Affichage de la réponse
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False)) 
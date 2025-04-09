import requests
import json
from datetime import datetime, timedelta

# URL de l'API
BASE_URL = "http://127.0.0.1:5000"

def test_project_activity():
    # 1. Authentification
    auth_data = {
        "username": "testuser",
        "password": "test123"
    }
    
    print("\n=== Authentification ===")
    auth_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=auth_data
    )
    
    if auth_response.status_code != 200:
        print("Erreur d'authentification:", auth_response.text)
        return
    
    token = auth_response.json()['access_token']
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. Création d'un projet
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)  # Un an plus tard
    
    project_data = {
        "name": "Projet de test",
        "description": "Ceci est un projet de test",
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "status": "active"
    }
    
    print("\n=== Création du projet ===")
    project_response = requests.post(
        f"{BASE_URL}/api/projects",
        headers=headers,
        json=project_data
    )
    
    print("Status Code:", project_response.status_code)
    print("Response:", json.dumps(project_response.json(), indent=2, ensure_ascii=False))
    
    if project_response.status_code != 201:
        print("Erreur lors de la création du projet")
        return
    
    project_id = project_response.json()['project']['id']
    
    # 3. Enregistrement d'une activité
    activity_data = {
        "action": "project_creation",
        "entity_type": "project",
        "entity_id": project_id,
        "details": "Projet créé avec succès",
        "ip_address": "127.0.0.1",
        "user_agent": "Test Script"
    }
    
    print("\n=== Enregistrement de l'activité ===")
    activity_response = requests.post(
        f"{BASE_URL}/api/activities",
        headers=headers,
        json=activity_data
    )
    
    print("Status Code:", activity_response.status_code)
    print("Response:", json.dumps(activity_response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_project_activity() 
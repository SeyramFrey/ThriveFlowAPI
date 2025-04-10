import os
from mistralai import Mistral
import logging
import json
import re
from datetime import datetime

class ProjectGenerator:
    def __init__(self):
        logging.info("=== Initialisation du ProjectGenerator ===")
        self.api_key = "6rJnvjrYHYNMR9yrWHT3u5o7AJjIRUPd"
        self.client = Mistral(api_key=self.api_key)
        logging.info("Client Mistral initialisé avec succès")

    def clean_json_string(self, json_str: str) -> str:
        """
        Nettoie une chaîne potentiellement mal formatée pour la rendre compatible JSON.
        """
        logging.info("Nettoyage de la chaîne JSON")
        
        # Enlever les backticks de code markdown s'ils existent
        json_str = re.sub(r'^```json\s*', '', json_str)
        json_str = re.sub(r'^```\s*', '', json_str)
        json_str = re.sub(r'\s*```$', '', json_str)
        
        # Détecter le début et la fin du JSON (entre accolades)
        match = re.search(r'(\{.*\})', json_str, re.DOTALL)
        if match:
            logging.info("JSON valide détecté par regex")
            return match.group(1)
            
        # Si aucun JSON valide n'est trouvé, retourner la chaîne originale
        return json_str

    def parse_json_safely(self, text: str) -> dict:
        """
        Tente de parser un JSON de manière sécurisée avec plusieurs méthodes.
        """
        logging.info("Tentative de parsing JSON sécurisé")
        
        # Première tentative: parsing direct
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logging.warning(f"Première tentative de parsing JSON échouée: {str(e)}")
            
        # Deuxième tentative: nettoyage puis parsing
        cleaned_text = self.clean_json_string(text)
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            logging.error(f"Deuxième tentative de parsing JSON échouée: {str(e)}")
            
            # Créer un JSON minimal valide avec le texte original
            return {
                "error": "Impossible de parser la réponse JSON",
                "original_text": text,
                "project": {
                    "name": "Projet par défaut",
                    "description": "Projet créé à partir d'une réponse non parsable"
                },
                "activities": []
            }

    def generate_project(self, idea: str) -> dict:
        try:
            logging.info("=== Début de generate_project ===")
            logging.info(f"Idée reçue : {idea}")
            
            logging.info("Préparation de la requête Mistral")
            messages = [
                {
                    "role": "user",
                    "content": idea
                },
            ]
            logging.info(f"Messages préparés : {messages}")
            
            logging.info("Envoi de la requête à l'API Mistral")
            chat_response = self.client.agents.complete(
                agent_id="ag:d6a2a39e:20250408:thriverflow-agent:70d068e5",
                messages=messages,
            )
            logging.info("Réponse reçue de l'API Mistral")
            logging.info(f"Réponse brute : {str(chat_response)}")
            
            generated_text = chat_response.choices[0].message.content
            logging.info(f"Texte généré : {generated_text[:200]}...")
            
            # Utiliser notre fonction de parsing JSON sécurisé
            parsed_json = self.parse_json_safely(generated_text)
            
            return {
                "raw_response": parsed_json,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Erreur dans generate_project : {str(e)}")
            logging.error(f"Type d'erreur : {type(e)}")
            raise

    def generate_project_from_idea(self, idea: str) -> dict:
        logging.info(f"Starting generate_project_from_idea with idea: {idea}")
        return self.generate_project(idea) 
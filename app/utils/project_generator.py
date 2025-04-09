import os
from mistralai import Mistral
import logging
import json
from datetime import datetime

class ProjectGenerator:
    def __init__(self):
        logging.info("=== Initialisation du ProjectGenerator ===")
        self.api_key = "6rJnvjrYHYNMR9yrWHT3u5o7AJjIRUPd"
        self.client = Mistral(api_key=self.api_key)
        logging.info("Client Mistral initialisé avec succès")

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
            
            return {
                "raw_response": json.loads(generated_text),
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
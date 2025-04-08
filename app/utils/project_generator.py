from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import Dict, List, Optional
import json

class ProjectGenerator:
    def __init__(self):
        self.model_name = "mistralai/Mixtral-8x7B-v0.1"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_8bit=True
        )
        
    def generate_project_from_idea(self, idea: str, context: Optional[Dict] = None) -> Dict:
        """
        Génère un projet structuré à partir d'une idée.
        
        Args:
            idea (str): L'idée de l'utilisateur
            context (Optional[Dict]): Contexte supplémentaire (objectifs, contraintes, etc.)
            
        Returns:
            Dict: Projet généré avec ses composants
        """
        # Construction du prompt
        prompt = self._build_prompt(idea, context)
        
        # Génération
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=1024,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        # Décodage de la réponse
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extraction et structuration des informations
        project = self._parse_response(response)
        
        return project
    
    def _build_prompt(self, idea: str, context: Optional[Dict] = None) -> str:
        """Construit le prompt pour le modèle."""
        prompt = f"""Tu es un expert en gestion de projet, en gestion de budget et en gestion de tâches. À partir de l'idée suivante, génère un projet structuré :

Idée : {idea}

Contexte : {json.dumps(context) if context else "Aucun contexte spécifique"}

Génère un projet avec les éléments suivants :
1. Nom du projet
2. Description détaillée
3. Objectifs principaux
4. Livrables attendus
5. Étapes principales
6. Ressources nécessaires
7. Contraintes potentielles
8. Critères de succès

Format de réponse en JSON :
{{
    "name": "Nom du projet",
    "description": "Description détaillée",
    "objectives": ["Objectif 1", "Objectif 2", ...],
    "deliverables": ["Livrable 1", "Livrable 2", ...],
    "milestones": [
        {{
            "name": "Nom de l'étape",
            "description": "Description",
            "due_date": "Date estimée"
        }},
        ...
    ],
    "resources": ["Ressource 1", "Ressource 2", ...],
    "constraints": ["Contrainte 1", "Contrainte 2", ...],
    "success_criteria": ["Critère 1", "Critère 2", ...]
}}
"""
        return prompt
    
    def _parse_response(self, response: str) -> Dict:
        """Extrait et structure les informations de la réponse du modèle."""
        try:
            # Extraction de la partie JSON de la réponse
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            # Conversion en dictionnaire
            project = json.loads(json_str)
            return project
        except Exception as e:
            print(f"Erreur lors de l'analyse de la réponse : {e}")
            return {
                "error": "Impossible de générer un projet structuré à partir de la réponse du modèle"
            } 
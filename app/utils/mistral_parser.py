import re
import json
import logging

logger = logging.getLogger(__name__)

def camel_to_snake(name):
    """Convertit un nom en camelCase en snake_case"""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def convert_keys_camel_to_snake(obj):
    """
    Convertit récursivement toutes les clés camelCase en snake_case dans un objet imbriqué
    """
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_key = camel_to_snake(key)
            new_dict[new_key] = convert_keys_camel_to_snake(value)
        return new_dict
    elif isinstance(obj, list):
        return [convert_keys_camel_to_snake(item) for item in obj]
    else:
        return obj

def extract_project_data(mistral_response):
    """
    Extrait et traite les données du projet à partir de la réponse de l'API Mistral
    """
    try:
        # Extraire les données du projet
        project_data = mistral_response.get('project', {})
        
        # Convertir les clés camelCase en snake_case
        project_data = convert_keys_camel_to_snake(project_data)
        
        # Assurer que les types de données sont corrects
        if 'key_points' in project_data and isinstance(project_data['key_points'], list):
            project_data['key_points'] = {
                'points': project_data['key_points']
            }
        
        return project_data
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des données du projet : {str(e)}")
        return {}

def extract_activities_data(mistral_response):
    """
    Extrait et traite les données des activités à partir de la réponse de l'API Mistral
    """
    try:
        # Extraire les activités
        activities_data = mistral_response.get('activities', [])
        
        # Convertir les clés camelCase en snake_case pour chaque activité
        activities_data = [convert_keys_camel_to_snake(activity) for activity in activities_data]
        
        # Convertir les ressources et dépendances en JSON pour chaque activité
        for activity in activities_data:
            if 'resources' in activity:
                activity['resources'] = json.dumps(activity['resources'])
            if 'dependencies' in activity:
                activity['dependencies'] = json.dumps(activity['dependencies'])
            # Assurer que les dates sont au format correct (si nécessaire)
            
        return activities_data
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des données des activités : {str(e)}")
        return []

def extract_project_summary(mistral_response):
    """
    Extrait et traite les données du résumé du projet
    """
    try:
        # Extraire les données du résumé du projet
        summary_data = mistral_response.get('projectSummary', {})
        
        # Convertir les clés camelCase en snake_case
        summary_data = convert_keys_camel_to_snake(summary_data)
        
        return summary_data
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des données du résumé : {str(e)}")
        return {}

def parse_mistral_response(mistral_response):
    """
    Parse la réponse complète de l'API Mistral et extrait toutes les données structurées
    """
    try:
        result = {
            'project': extract_project_data(mistral_response),
            'activities': extract_activities_data(mistral_response),
            'project_summary': extract_project_summary(mistral_response)
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Erreur lors du parsing de la réponse Mistral : {str(e)}")
        return {
            'project': {},
            'activities': [],
            'project_summary': {}
        } 
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.project_generator import ProjectGenerator
from app.utils.mistral_parser import parse_mistral_response
from app.models import db
from app.models.idea import Idea
from app.models.project import Project
from app.models.activity import Activity
from app.models.user import User
from datetime import datetime
import logging
import jwt
import json
import re

project_gen_bp = Blueprint('project_generation', __name__)
project_generator = ProjectGenerator()

@project_gen_bp.route('/generate-project', methods=['POST'])
def generate_project():
    logging.info("=== ROUTE /generate-project APPELÉE ===")
    
    # Log des headers mais en masquant les informations sensibles
    headers_log = {k: v for k, v in request.headers.items()}
    if 'Authorization' in headers_log:
        headers_log['Authorization'] = headers_log['Authorization'][:20] + '...'
    logging.info(f"Headers: {headers_log}")
    
    auth_header = request.headers.get('Authorization', '')
    logging.info(f"Auth header présent: {'Authorization' in request.headers}")
    
    if not auth_header.startswith('Bearer '):
        logging.error("Token manquant ou format incorrect")
        return jsonify({'msg': 'Missing Bearer token'}), 401
        
    # Récupération du token    
    token = auth_header.split(' ')[1]
    logging.info(f"Token récupéré (premiers caractères): {token[:10]}...")
    
    try:
        # Importation de PyJWT pour décoder manuellement le token
        import jwt
        from flask import current_app
        
        # Récupérer la clé secrète
        secret_key = current_app.config['JWT_SECRET_KEY']
        
        # Décoder le token sans vérification du sujet
        try:
            # Décoder sans validation complète
            decoded_token = jwt.decode(
                token, 
                secret_key,
                options={"verify_signature": True, "verify_exp": True},
                algorithms=["HS256"]
            )
            
            # Extraire et convertir l'identité en string manuellement
            user_id = str(decoded_token['sub'])
            logging.info(f"ID utilisateur extrait manuellement: {user_id}")
            
        except Exception as e:
            logging.error(f"Erreur lors du décodage manuel du token: {str(e)}")
            return jsonify({'msg': f'Invalid token: {str(e)}'}), 422
        
        logging.info("=== JWT vérifié avec succès ===")
        logging.info("=== Début de la fonction generate_project ===")
        
        # Convertir l'ID en entier pour la requête à la base de données
        try:
            user_id_int = int(user_id)
            logging.info(f"User ID converti en int: {user_id_int}")
        except ValueError:
            logging.error(f"Impossible de convertir l'ID utilisateur en entier: {user_id}")
            return jsonify({'error': 'Invalid user ID format'}), 400
            
        user = User.query.get(user_id_int)
        logging.info(f"User found: {user}")
        
        if not user:
            logging.error("User not found")
            return jsonify({'error': 'User not found'}), 404
            
        data = request.get_json()
        logging.info(f"Request data: {data}")
        
        if not data:
            logging.error("No data provided in request")
            return jsonify({'error': 'No data provided'}), 400
            
        if 'idea' not in data:
            logging.error("No idea provided in request")
            return jsonify({'error': 'Idea is required'}), 400
            
        # Vérifier si l'idée est trop courte
        if len(data['idea'].strip()) < 10:
            logging.error("Idée trop courte")
            return jsonify({
                'success': False,
                'error': 'Idée trop courte',
                'message': "Veuillez fournir une idée plus détaillée pour générer un projet.",
                'rejectResponse': True
            }), 400
            
        # Enregistrer l'idée de l'utilisateur
        try:
            idea = Idea(
                title=f"Idée: {data['idea'][:50]}...",  # Limiter la longueur du titre
                description=data['idea'],
                user_id=user_id_int
            )
            db.session.add(idea)
            db.session.commit()
            logging.info(f"Idée enregistrée avec l'ID: {idea.id}")
        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement de l'idée: {str(e)}")
            db.session.rollback()
            return jsonify({'error': f'Failed to save idea: {str(e)}'}), 500
            
        # Génération du projet
        try:
            logging.info("=== Début de la génération du projet ===")
            logging.info(f"Appel de generate_project avec l'idée: {data['idea']}")
            generated_project = project_generator.generate_project(data['idea'])
            logging.info(f"Project generated successfully: {generated_project}")
            
            # Vérifier si une erreur est présente dans la réponse
            if generated_project.get("raw_response", {}).get("error"):
                error_msg = generated_project["raw_response"]["error"]
                logging.error(f"Erreur détectée dans la réponse: {error_msg}")
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'message': "Le format de la réponse reçue n'est pas valide. Veuillez reformuler votre idée.",
                    'rejectResponse': True
                }), 422
            
            # Retourner le JSON avec l'ID de l'idée pour pouvoir la retrouver
            return jsonify({
                'success': True,
                'data': generated_project,
                'idea_id': idea.id
            }), 200
            
        except Exception as e:
            logging.error(f"Error generating project: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': "Une erreur s'est produite lors de la génération du projet. Veuillez essayer avec une autre idée.",
                'rejectResponse': True
            }), 422
            
    except Exception as e:
        logging.error(f"JWT Error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'JWT validation failed: {str(e)}',
            'message': "Votre session a expiré. Veuillez vous reconnecter.",
            'rejectResponse': True
        }), 422

@project_gen_bp.route('/save-generated-project', methods=['POST'])
@jwt_required()
def save_generated_project():
    """
    Endpoint pour enregistrer un projet généré par l'API Mistral
    
    Paramètres attendus dans le corps de la requête:
    - mistral_response: La réponse brute de l'API Mistral
    - idea_id: L'ID de l'idée associée (optionnel)
    """
    logging.info("=== ROUTE /save-generated-project APPELÉE ===")
    
    try:
        # Récupérer l'ID de l'utilisateur authentifié
        current_user_id = get_jwt_identity()
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        logging.info(f"Utilisateur authentifié: {current_user_id}")
        
        # Récupérer les données de la requête
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Vérifier que la réponse Mistral est présente
        if 'mistral_response' not in data:
            return jsonify({'error': 'Mistral response is required'}), 400
        
        mistral_response = data['mistral_response']
        idea_id = data.get('idea_id')
        
        # Vérifier si la réponse Mistral contient une erreur
        if isinstance(mistral_response, dict) and mistral_response.get("error"):
            error_msg = mistral_response["error"]
            logging.error(f"Erreur détectée dans la réponse Mistral: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg,
                'message': "La réponse Mistral contient une erreur. Impossible de sauvegarder le projet."
            }), 422
        
        # Utiliser notre parseur pour extraire les données structurées
        try:
            parsed_data = parse_mistral_response(mistral_response)
            logging.info(f"Données parsées et prêtes à être enregistrées")
            
            # Vérifier que les données requises sont présentes
            if not parsed_data.get('project') or not parsed_data.get('activities'):
                logging.error("Données manquantes dans la réponse parsée")
                return jsonify({
                    'success': False,
                    'error': 'Missing required data in parsed response',
                    'message': "Les données nécessaires à la création du projet sont manquantes."
                }), 422
        except Exception as e:
            logging.error(f"Erreur lors du parsing des données: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': "Impossible de traiter les données reçues. Veuillez réessayer."
            }), 422
        
        # Commencer une transaction pour garantir l'intégrité des données
        try:
            # Créer le projet avec les données parsées
            project_data = parsed_data['project']
            
            # Ajouter les informations obligatoires
            project_data['user_id'] = current_user_id
            
            # Créer le projet
            project = Project(**project_data)
            db.session.add(project)
            db.session.flush()  # Pour obtenir l'ID du projet
            
            logging.info(f"Projet créé temporairement avec ID: {project.id}")
            
            # Si une idée est fournie, la mettre à jour avec l'ID du projet
            if idea_id:
                idea = Idea.query.get(idea_id)
                if idea and idea.user_id == current_user_id:
                    idea.project_id = project.id
                    logging.info(f"Idée {idea_id} associée au projet {project.id}")
            
            # Créer les activités associées au projet
            created_activities = []
            for activity_data in parsed_data['activities']:
                # Ajouter les informations obligatoires
                activity_data['user_id'] = current_user_id
                activity_data['project_id'] = project.id
                
                # Créer l'activité
                activity = Activity(**activity_data)
                db.session.add(activity)
                created_activities.append(activity)
            
            # Valider la transaction
            db.session.commit()
            
            logging.info(f"Projet et activités sauvegardés avec succès. Projet ID: {project.id}")
            
            # Préparer la réponse
            response = {
                'success': True,
                'message': 'Project and activities saved successfully',
                'project': {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'status': project.status,
                    'activities_count': len(created_activities)
                }
            }
            
            return jsonify(response), 201
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erreur lors de l'enregistrement du projet et des activités: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': "Une erreur s'est produite lors de l'enregistrement du projet."
            }), 500
            
    except Exception as e:
        logging.error(f"Erreur générale: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "Une erreur s'est produite lors du traitement de la requête."
        }), 500 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.models.activity import  Activity
from app.models.project import Project
from datetime import datetime
import logging

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/activities', methods=['POST'])
@jwt_required()
def create_activity():
    try:
        current_user_id = get_jwt_identity()
        # Convertir l'ID utilisateur en entier si c'est une chaîne
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
            
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['name', 'project_id', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Vérifier si le projet existe
        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Vérifier si l'utilisateur a accès au projet
        if project.user_id != current_user_id:
            return jsonify({'error': 'You do not have access to this project'}), 403
        
        activity = Activity(
            name=data['name'],
            description=data['description'],
            project_id=data['project_id'],
            user_id=current_user_id,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            estimated_daily_time=data.get('estimated_daily_time'),
            estimated_duration=data.get('estimated_duration'),
            estimated_cost=data.get('estimated_cost'),
            status=data.get('status', 'not started'),
            priority=data.get('priority', 'medium'),
            dependencies=data.get('dependencies'),
            resources=data.get('resources')
        )
        
        db.session.add(activity)
        db.session.commit()
        
        # Enregistrer l'action dans l'historique
        create_activity_record(current_user_id, 'create', 'activity', activity.id, 
                               f"Activity '{activity.name}' created for project '{project.name}'")
        
        return jsonify({
            'message': 'Activity created successfully',
            'activity': {
                'id': activity.id,
                'name': activity.name,
                'description': activity.description,
                'project_id': activity.project_id,
                'status': activity.status,
                'created_at': activity.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating activity: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/activities/<int:activity_id>', methods=['GET'])
@jwt_required()
def get_activity(activity_id):
    try:
        current_user_id = get_jwt_identity()
        # Convertir l'ID utilisateur en entier si c'est une chaîne
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
            
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Vérifier si l'utilisateur a accès à l'activité
        if activity.user_id != current_user_id:
            return jsonify({'error': 'You do not have access to this activity'}), 403
        
        return jsonify({
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'project_id': activity.project_id,
            'start_date': activity.start_date.isoformat() if activity.start_date else None,
            'end_date': activity.end_date.isoformat() if activity.end_date else None,
            'estimated_daily_time': activity.estimated_daily_time,
            'estimated_duration': activity.estimated_duration,
            'estimated_cost': activity.estimated_cost,
            'status': activity.status,
            'priority': activity.priority,
            'dependencies': activity.dependencies,
            'resources': activity.resources,
            'created_at': activity.created_at.isoformat(),
            'updated_at': activity.updated_at.isoformat()
        }), 200
        
    except Exception as e:
        logging.error(f"Error retrieving activity: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Fonction utilitaire pour créer une entrée d'activité dans l'historique
def create_activity_record(user_id, action, entity_type, entity_id, details):
    # Cette fonction est utilisée pour enregistrer les actions des utilisateurs
    # dans un journal d'activité séparé (qui pourrait être implémenté plus tard)
    logging.info(f"Activity recorded: User {user_id} performed {action} on {entity_type} {entity_id}: {details}")
    return True 
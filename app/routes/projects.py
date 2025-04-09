from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.models.project import Project
from app.models.activity import Activity
from app.models.idea import Idea
import logging
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        current_user_id = get_jwt_identity()
        # Convertir l'ID utilisateur en entier si c'est une chaîne
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
            
        logging.info(f"Récupération des projets pour l'utilisateur {current_user_id}")
        
        projects = Project.query.filter_by(user_id=current_user_id).all()
        logging.info(f"Nombre de projets trouvés: {len(projects)}")
        
        result = []
        
        for project in projects:
            # Récupérer les activités associées au projet
            activities = Activity.query.filter_by(project_id=project.id).all()
            
            # Récupérer l'idée associée au projet
            idea = Idea.query.filter_by(project_id=project.id).first()
            
            project_data = {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'status': project.status,
                'start_date': project.start_date.isoformat() if project.start_date else None,
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'estimated_budget': project.estimated_budget,
                'estimated_duration': project.estimated_duration,
                'competitive_advantage': project.competitive_advantage,
                'key_points': project.key_points,
                'created_at': project.created_at.isoformat(),
                'activities': [
                    {
                        'id': activity.id,
                        'name': activity.name,
                        'description': activity.description,
                        'status': activity.status,
                        'start_date': activity.start_date.isoformat() if activity.start_date else None,
                        'end_date': activity.end_date.isoformat() if activity.end_date else None,
                        'estimated_duration': activity.estimated_duration,
                        'estimated_cost': activity.estimated_cost,
                        'priority': activity.priority
                    } for activity in activities
                ],
                'idea': {
                    'id': idea.id,
                    'title': idea.title,
                    'description': idea.description
                } if idea else None
            }
            
            result.append(project_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        logging.error(f"Error retrieving projects: {str(e)}")
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    try:
        current_user_id = get_jwt_identity()
        # Convertir l'ID utilisateur en entier si c'est une chaîne
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
            
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Créer le projet
        project = Project(
            name=data['name'],
            description=data['description'],
            user_id=current_user_id,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            status=data.get('status', 'planning'),
            estimated_budget=data.get('estimated_budget'),
            estimated_duration=data.get('estimated_duration'),
            competitive_advantage=data.get('competitive_advantage'),
            key_points=data.get('key_points')
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Créer l'idée si elle est fournie
        if 'idea' in data:
            idea = Idea(
                title=f"Idée: {project.name}",
                description=data['idea'],
                user_id=current_user_id,
                project_id=project.id
            )
            db.session.add(idea)
            db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project': {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'status': project.status,
                'created_at': project.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating project: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        # Convertir l'ID utilisateur en entier si c'est une chaîne
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
            
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Vérifier si l'utilisateur a accès au projet
        if project.user_id != current_user_id:
            return jsonify({'error': 'You do not have access to this project'}), 403
        
        # Récupérer les activités associées au projet
        activities = Activity.query.filter_by(project_id=project.id).all()
        
        # Récupérer l'idée associée au projet
        idea = Idea.query.filter_by(project_id=project.id).first()
        
        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'status': project.status,
            'start_date': project.start_date.isoformat() if project.start_date else None,
            'end_date': project.end_date.isoformat() if project.end_date else None,
            'estimated_budget': project.estimated_budget,
            'estimated_duration': project.estimated_duration,
            'competitive_advantage': project.competitive_advantage,
            'key_points': project.key_points,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat(),
            'activities': [
                {
                    'id': activity.id,
                    'name': activity.name,
                    'description': activity.description,
                    'status': activity.status,
                    'start_date': activity.start_date.isoformat() if activity.start_date else None,
                    'end_date': activity.end_date.isoformat() if activity.end_date else None,
                    'estimated_duration': activity.estimated_duration,
                    'estimated_cost': activity.estimated_cost,
                    'priority': activity.priority
                } for activity in activities
            ],
            'idea': {
                'id': idea.id,
                'title': idea.title,
                'description': idea.description
            } if idea else None
        }), 200
        
    except Exception as e:
        logging.error(f"Error retrieving project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'start_date' in data:
            project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        if 'end_date' in data:
            project.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        if 'status' in data:
            project.status = data['status']
            
        db.session.commit()
        
        return jsonify({
            'message': 'Project updated successfully',
            'project': {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
                'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
                'status': project.status
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error updating project: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
            
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'}), 200
        
    except Exception as e:
        logging.error(f"Error deleting project: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
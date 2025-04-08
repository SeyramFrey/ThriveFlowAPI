from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.project_generator import ProjectGenerator
from app.models import db, Project, Task, Category, Tag
from datetime import datetime

project_gen_bp = Blueprint('project_generation', __name__)
project_generator = ProjectGenerator()

@project_gen_bp.route('/api/generate-project', methods=['POST'])
@jwt_required()
def generate_project():
    try:
        data = request.get_json()
        idea = data.get('idea')
        context = data.get('context', {})
        
        if not idea:
            return jsonify({'error': 'L\'idée est requise'}), 400
        
        # Génération du projet
        generated_project = project_generator.generate_project_from_idea(idea, context)
        
        if 'error' in generated_project:
            return jsonify(generated_project), 500
        
        # Création du projet dans la base de données
        user_id = get_jwt_identity()
        
        # Création du projet principal
        project = Project(
            user_id=user_id,
            name=generated_project['name'],
            description=generated_project['description'],
            start_date=datetime.now().date(),
            status='active'
        )
        db.session.add(project)
        db.session.flush()  # Pour obtenir l'ID du projet
        
        # Création des catégories pour les objectifs
        for objective in generated_project['objectives']:
            category = Category(
                project_id=project.id,
                name=objective,
                description=f"Catégorie pour l'objectif : {objective}",
                color="#FF0000"  # Couleur par défaut
            )
            db.session.add(category)
        
        # Création des tâches pour les étapes principales
        for milestone in generated_project['milestones']:
            task = Task(
                project_id=project.id,
                created_by_id=user_id,
                title=milestone['name'],
                description=milestone['description'],
                due_date=datetime.strptime(milestone['due_date'], '%Y-%m-%d').date(),
                status='todo'
            )
            db.session.add(task)
        
        # Création des tags pour les ressources et contraintes
        for resource in generated_project['resources']:
            tag = Tag(
                project_id=project.id,
                name=resource,
                color="#00FF00"  # Couleur par défaut pour les ressources
            )
            db.session.add(tag)
        
        for constraint in generated_project['constraints']:
            tag = Tag(
                project_id=project.id,
                name=constraint,
                color="#FF0000"  # Couleur par défaut pour les contraintes
            )
            db.session.add(tag)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Projet généré avec succès',
            'project': {
                'id': project.id,
                'name': project.name,
                'description': project.description
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
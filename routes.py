from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import db, User, Project, Task, Expense, Suggestion
from datetime import datetime

# Auth Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        email=data['email'],
        full_name=data.get('full_name')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

# Project Blueprint
project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    user_id = get_jwt_identity()
    projects = Project.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'goal': p.goal,
        'start_date': p.start_date.isoformat() if p.start_date else None,
        'expected_end_date': p.expected_end_date.isoformat() if p.expected_end_date else None,
        'progress_percent': p.progress_percent
    } for p in projects]), 200

@project_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    project = Project(
        user_id=get_jwt_identity(),
        title=data['title'],
        description=data.get('description'),
        goal=data.get('goal'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
        expected_end_date=datetime.strptime(data['expected_end_date'], '%Y-%m-%d').date() if data.get('expected_end_date') else None
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({'message': 'Project created successfully', 'id': project.id}), 201

# Task Blueprint
task_bp = Blueprint('task', __name__)

@task_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_tasks(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'is_done': t.is_done,
        'estimated_time_hours': t.estimated_time_hours,
        'real_time_hours': t.real_time_hours
    } for t in tasks]), 200

@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    task = Task(
        project_id=data['project_id'],
        title=data['title'],
        estimated_time_hours=data.get('estimated_time_hours')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'message': 'Task created successfully', 'id': task.id}), 201

# Expense Blueprint
expense_bp = Blueprint('expense', __name__)

@expense_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_expenses(project_id):
    expenses = Expense.query.filter_by(project_id=project_id).all()
    return jsonify([{
        'id': e.id,
        'description': e.description,
        'amount': float(e.amount),
        'date_spent': e.date_spent.isoformat(),
        'category': e.category
    } for e in expenses]), 200

@expense_bp.route('/', methods=['POST'])
@jwt_required()
def create_expense():
    data = request.get_json()
    expense = Expense(
        project_id=data['project_id'],
        description=data.get('description'),
        amount=data['amount'],
        category=data.get('category')
    )
    
    db.session.add(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense created successfully', 'id': expense.id}), 201

# Suggestion Blueprint
suggestion_bp = Blueprint('suggestion', __name__)

@suggestion_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_suggestions(project_id):
    suggestions = Suggestion.query.filter_by(project_id=project_id).all()
    return jsonify([{
        'id': s.id,
        'text': s.text,
        'suggestion_type': s.suggestion_type
    } for s in suggestions]), 200

@suggestion_bp.route('/', methods=['POST'])
@jwt_required()
def create_suggestion():
    data = request.get_json()
    suggestion = Suggestion(
        project_id=data['project_id'],
        text=data['text'],
        suggestion_type=data.get('suggestion_type')
    )
    
    db.session.add(suggestion)
    db.session.commit()
    
    return jsonify({'message': 'Suggestion created successfully', 'id': suggestion.id}), 201 
from datetime import datetime
from app import db
from app.models.user import User
from app.models.idea import Idea

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='planning')  # planning, active, completed, on_hold
    estimated_budget = db.Column(db.Float)
    estimated_duration = db.Column(db.String(50))
    competitive_advantage = db.Column(db.Text)
    key_points = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    idea = db.relationship('Idea', backref='project', uselist=False, lazy=True)

    def __init__(self, name, user_id, description=None, start_date=None, end_date=None, 
                 status='planning', estimated_budget=None, estimated_duration=None,
                 competitive_advantage=None, key_points=None):
        self.name = name
        self.user_id = user_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.estimated_budget = estimated_budget
        self.estimated_duration = estimated_duration
        self.competitive_advantage = competitive_advantage
        self.key_points = key_points
    
    def __repr__(self):
        return f'<Project {self.name}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')
    priority = db.Column(db.String(20), default='medium')
    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    estimated_daily_time = db.Column(db.String(50))
    estimated_duration = db.Column(db.String(50))
    estimated_cost = db.Column(db.Float)
    dependencies = db.Column(db.JSON)  # Stockage des dépendances sous forme de JSON
    resources = db.Column(db.JSON)  # Stockage des ressources sous forme de JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = db.relationship('Category', backref='tasks')
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_tasks')
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_tasks')
    parent = db.relationship('Task', remote_side=[id], backref='subtasks')
    tags = db.relationship('Tag', secondary='task_tags', backref='tasks')
    comments = db.relationship('Comment', backref='task', cascade='all, delete-orphan')

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='comments')
    parent = db.relationship('Comment', remote_side=[id], backref='replies')
    project = db.relationship('Project', backref='comments')

# Table d'association pour les tags des tâches
task_tags = db.Table('task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
) 
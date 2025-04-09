from datetime import datetime
from app import db
from app.models.user import User
from app.models.project import Project

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    estimated_daily_time = db.Column(db.String(50))
    estimated_duration = db.Column(db.String(50))
    estimated_cost = db.Column(db.Float)
    status = db.Column(db.String(20), default='not started')  # not started, in progress, completed, delayed
    priority = db.Column(db.String(20), default='medium')     # low, medium, high
    dependencies = db.Column(db.JSON)  # Stockage des dépendances sous forme de JSON
    resources = db.Column(db.JSON)     # Stockage des ressources sous forme de JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, project_id, user_id, description=None, start_date=None,
                 end_date=None, estimated_daily_time=None, estimated_duration=None,
                 estimated_cost=None, status='not started', priority='medium',
                 dependencies=None, resources=None):
        self.name = name
        self.project_id = project_id
        self.user_id = user_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.estimated_daily_time = estimated_daily_time
        self.estimated_duration = estimated_duration
        self.estimated_cost = estimated_cost
        self.status = status
        self.priority = priority
        self.dependencies = dependencies
        self.resources = resources
    
    def __repr__(self):
        return f'<Activity {self.name}>' 
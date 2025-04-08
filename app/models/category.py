from datetime import datetime
from .user import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    color = db.Column(db.String(7))  # Format hexadécimal (#RRGGBB)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('categories', lazy=True))
    
    # Tasks relationship will be defined in the Task model
    
    def __init__(self, name, project_id, description=None, color=None):
        self.name = name
        self.project_id = project_id
        self.description = description
        self.color = color
    
    def __repr__(self):
        return f'<Category {self.name}>' 
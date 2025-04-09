from datetime import datetime
from app import db

class Idea(db.Model):
    __tablename__ = 'ideas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    creator = db.relationship('User', backref='created_ideas', overlaps="ideas", foreign_keys=[user_id])
    
    def __init__(self, title, description, user_id, project_id=None):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.project_id = project_id
    
    def __repr__(self):
        return f'<Idea {self.title}>' 
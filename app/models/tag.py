from datetime import datetime
from .user import db

# Table d'association entre Tag et Task
task_tags = db.Table('task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    color = db.Column(db.String(7))  # Format hexadécimal (#RRGGBB)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('tags', lazy=True))
    
    # Relation many-to-many avec Task
    tasks = db.relationship('Task', secondary=task_tags, lazy='subquery',
                          backref=db.backref('tags', lazy=True))
    
    def __init__(self, name, project_id, color=None):
        self.name = name
        self.project_id = project_id
        self.color = color
    
    def __repr__(self):
        return f'<Tag {self.name}>' 
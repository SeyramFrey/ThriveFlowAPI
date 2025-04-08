from datetime import datetime
from .user import db

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, done, blocked
    priority = db.Column(db.Integer, default=0)  # 0=low, 1=medium, 2=high, 3=urgent
    due_date = db.Column(db.DateTime)
    estimated_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relations
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('tasks', lazy=True))
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))
    
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assignee = db.relationship('User', backref=db.backref('assigned_tasks', lazy=True))
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', foreign_keys=[creator_id], backref=db.backref('created_tasks', lazy=True))
    
    parent_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    subtasks = db.relationship('Task', backref=db.backref('parent', remote_side=[id]))
    
    def __init__(self, title, project_id, creator_id, description=None, category_id=None, 
                 assignee_id=None, due_date=None, estimated_hours=None, priority=0):
        self.title = title
        self.project_id = project_id
        self.creator_id = creator_id
        self.description = description
        self.category_id = category_id
        self.assignee_id = assignee_id
        self.due_date = due_date
        self.estimated_hours = estimated_hours
        self.priority = priority
    
    def complete(self):
        self.status = 'done'
        self.completed_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Task {self.title}>' 
from datetime import datetime
from app.models import db

class Task(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    
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
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    
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
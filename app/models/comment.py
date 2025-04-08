from datetime import datetime
from .user import db

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('comments', lazy=True, order_by='Comment.created_at'))
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))
    
    def __init__(self, content, task_id, author_id, parent_id=None):
        self.content = content
        self.task_id = task_id
        self.author_id = author_id
        self.parent_id = parent_id
    
    def __repr__(self):
        return f'<Comment {self.id} on Task {self.task_id}>' 
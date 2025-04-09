from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from app.models.user import User
from app import db
from datetime import timedelta
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    print("register")
    try:
        data = request.get_json()

        print(data)
        
        if not data:
            return jsonify({'message': 'No input data provided'}), 400
            
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        # Extract profile fields
        profile_fields = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'profession': data.get('profession'),
            'company': data.get('company'),
            'bio': data.get('bio'),
            'interests': data.get('interests', []),
            'skills': data.get('skills', []),
            'preferred_project_types': data.get('preferred_project_types', []),
            'time_availability': data.get('time_availability'),
            'preferred_working_hours': data.get('preferred_working_hours')
        }
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            **profile_fields
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logging.error(f"Error in register route: {str(e)}")
        db.session.rollback()
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No input data provided'}), 400
            
        # Validate required fields
        if 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.verify_password(data['password']):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }), 200
        
        return jsonify({'message': 'Invalid credentials'}), 401
        
    except Exception as e:
        logging.error(f"Error in login route: {str(e)}")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        # Assurez-vous que l'identité est une chaîne
        if not isinstance(current_user, str):
            current_user = str(current_user)
        new_token = create_access_token(identity=current_user, fresh=False)
        return jsonify({'access_token': new_token}), 200
    except Exception as e:
        logging.error(f"Error in refresh route: {str(e)}")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Dans une application réelle, vous voudriez peut-être blacklister le token
        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        logging.error(f"Error in logout route: {str(e)}")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500 
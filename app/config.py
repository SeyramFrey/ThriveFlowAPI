import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:3009@localhost:5432/thriveflow')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 24 heures 
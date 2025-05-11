import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'garv-secret-key-2024')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000)) 
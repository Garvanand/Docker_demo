from flask import Flask
from pythonjsonlogger import jsonlogger
import os

def create_app():
    app = Flask(__name__)
    logger = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    app.config.from_object('app.config.Config')
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    return app 
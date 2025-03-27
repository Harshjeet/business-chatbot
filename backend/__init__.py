from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API'),
        # 'RATE_LIMIT': "10/minute"
    })
    
    # from .views import limiter
    # limiter.init_app(app)
    
    return app
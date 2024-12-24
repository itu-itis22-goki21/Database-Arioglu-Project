from flask import Flask
from app.routes.coaches import coaches_bp
from app.routes.country import country_bp
from app.routes.medal import medal_bp
from app.routes.tech import tech_bp
from app.routes.athletes import athletes_bp
from app.routes.discipline import discipline_bp
from app.routes.events import events_bp
from app.routes.statistic import statistic_bp
from app.routes import main_bp

def create_app():
    app = Flask(__name__, template_folder='../templates')
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(coaches_bp, url_prefix='/coaches')
    app.register_blueprint(country_bp, url_prefix='/country')
    app.register_blueprint(medal_bp, url_prefix='/medal')
    app.register_blueprint(tech_bp, url_prefix='/tech')
    app.register_blueprint(athletes_bp, url_prefix='/athletes')
    app.register_blueprint(discipline_bp, url_prefix='/discipline')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(statistic_bp, url_prefix='/statistic')
    return app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from app.config import Config

# App instance 
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()



# Create App BluePrint 
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Migrate AFTER app is defined
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    
    from app.main.routes import main
    from app.users.routes import users
    from app.product.routes import product
    from app.errors.handlers import errors
    
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(product)
    app.register_blueprint(errors)
    
    
        
    
    return app

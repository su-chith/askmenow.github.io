from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os


db = SQLAlchemy()
DB_NAME = "new.db"




def create_app():
    app = Flask(__name__, static_folder='static')
   
    app.config['SECRET_KEY'] = 'secret'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Question, Category, Answer



    with app.app_context():
        # Category.__table__.drop(db.engine)
        
        db.create_all()
        # category1 = Category(name='Technology')
        # category2 = Category(name='Sports')
        # category3 = Category(name='Music')

        # db.session.add_all([category1, category2, category3])
        db.session.commit()
        

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_db():
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=create_app())
        print('Created Database!')



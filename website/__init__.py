from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    #sess = Session()


    from .views import views
    from .auth import auth
    from product_database import my_connection

    db_cursor = my_connection.cursor(buffered=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(currentUser):
        return db_cursor.execute(""""Select email from customers """)
         

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app

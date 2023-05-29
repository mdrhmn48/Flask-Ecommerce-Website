from flask import Flask
from flask_login import LoginManager, UserMixin


app = Flask(__name__)

def create_app():
    # app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    #sess = Session()


    from .views import views
    from .auth import auth
    from database_source_files.product_database import my_connection

    db_cursor = my_connection.cursor(buffered=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(currentUser):
        currentUser = db_cursor.execute("SELECT email FROM customers WHERE email = %s", (currentUser,))
        result = db_cursor.fetchone()
        if result:
        # Create a User object with the user ID (email)
            currentUser = UserMixin()
            currentUser.id = result[0]
            return currentUser
        else:
            return None
         

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app


if __name__== "__main__":
    app.run(debug=True)
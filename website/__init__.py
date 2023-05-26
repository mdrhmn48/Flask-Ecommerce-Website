from flask import Flask, Blueprint
from flask_login import LoginManager, UserMixin

from database_source_files.product_database import my_connection


from .views import views
from .auth import auth

db_connection = my_connection

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    db_cursor = db_connection.cursor(buffered=True)
    db_cursor.execute("SELECT email FROM customers WHERE email = %s", (user_id,))
    result = db_cursor.fetchone()
    print("user_id: ", result[0])
    db_cursor.close()
    if result:
        return User(result[0])
    else:
        return None
    
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super secret key'

    login_manager.init_app(app)
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
from flask import Blueprint, render_template
from database_source_files.product_database import get_products
from flask_login import  login_required, login_user, current_user
from database_source_files.product_database import my_connection

db_cursor = my_connection.cursor(buffered=True)

views = Blueprint("views", __name__)
# @login_required
@views.route("/", methods= ["GET", "POST"])
@login_required
def home():

    db_cursor.execute("""SELECT * FROM products""")
    result = db_cursor.fetchall()
    print(result)

    return render_template("home.html", currentUser=current_user, result=result)

# ... other code ...


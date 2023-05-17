from flask import Blueprint, render_template
from database_source_files.product_database import get_products
from flask_login import  login_required, login_user, current_user

views = Blueprint("views", __name__)

@views.route("/", methods= ["GET", "POST"])
# @login_required
def home():
    return render_template("home.html", title = 'Home', result=get_products("Vegetables"), foo=y, max=max_price(), prod_cat=product_category(), currentUser=current_user)
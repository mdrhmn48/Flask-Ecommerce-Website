from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from database_source_files.product_database import get_products
from flask_login import  login_required, login_user, current_user
from database_source_files.product_database import my_connection

views = Blueprint("views", __name__)


@views.route("/", methods= ["GET", "POST"])
@login_required
def home():
    current_user_email = current_user.id
    
    with my_connection.cursor(buffered=True) as db_cursor:
        db_cursor.execute("""SELECT * FROM products""")
        result = db_cursor.fetchall()
    
    total_price = 0
    if request.method == "POST":
        product_id  = int(request.form.get("product"))
        quantity = int(request.form.get("quantity"))
        current_user_email = current_user.id
        print(f"prod_name: {product_id }, {quantity}")
        product = get_product_from_database(product_id)
        print("product: ",product)
        if product is not None:
            if quantity > 0 and product[2] >= quantity:
                total_price = product[3] * quantity
                update_order_in_database(product_id, quantity)
                flash(f"{current_user_email} Order Placed Successfully! Your Total: {total_price}", category="success")
                return redirect(url_for('views.home', total_price = total_price))
            else:
                flash(f"We are out of stock on {product[1]}! Try a different quantity.", category="error")
        else:
            flash("Invalid product selected! Try again.", category="error")
    total_price = request.form.get('total_price', total_price)
    return render_template("home.html", currentUser=current_user_email, result=result, total_price = total_price)

# ... other code ...
def get_product_from_database(product_id):
    with my_connection.cursor(buffered=True) as db_cursor:
        db_query = "SELECT * FROM products WHERE product_id = %s"
        db_cursor.execute(db_query, (product_id,))
        product = db_cursor.fetchone()
        return product


def update_order_in_database(product_id, quantity):
    with my_connection.cursor(buffered=True) as db_cursor:
        db_query = "UPDATE products SET product_quantity = product_quantity - %s WHERE product_id = %s"
        db_cursor.execute(db_query, (quantity, product_id))
        my_connection.commit()


def get_all_product_from_database():
    with my_connection.cursor(buffered=True) as db_cursor:
        query = "SELECT * FROM products"
        db_cursor.execute(query)
        products = db_cursor.fetchall()
        return products


from flask import Blueprint, render_template, request,session, flash, redirect, url_for
from flask_login import login_required, current_user
from database_source_files.product_database import my_connection

views = Blueprint("views", __name__)





















@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    current_user_email = current_user.first_name
    print("current_user_email: ", current_user_email)

    with my_connection.cursor(buffered=True) as db_cursor:
        db_cursor.execute("SELECT * FROM products")
        result = db_cursor.fetchall()
        print("result:----->", result)

    if request.method == "POST":
        cart_items = []
        total_price = 0
        proceed_to_checkout = False  # Flag to check if it's valid to proceed to checkout

        for row in result:
            product_id = row[0]
            print("product_id:", product_id)
            quantity_str = request.form.get("quantity_" + str(product_id))

            print("quantity String: ", quantity_str)

            try:
                quantity = int(quantity_str)
                print("quantity: ", quantity)
                if quantity > 0:
                    product = get_product_from_database(product_id)
                    print(f"product_quan:,{product['product_quantity']}")
                    print("print: ", product)
                    if product is not None and product["product_quantity"] >= quantity:
                            item_price = product["product_price"] * quantity
                            total_price += item_price
                            total_price = round(total_price, 2)
                            print(total_price)
                            cart_item = {
                                "product_name": product["product_name"],
                                "quantity": quantity,
                                "price": product["product_price"],
                                "total": item_price
                            }
                            cart_items.append(cart_item)
                            print(cart_items)
                            update_order_in_database(product_id, quantity)
                            flash(f"{product['product_name']} added to cart.", category="success")
                            proceed_to_checkout = True  # Set flag to True if at least one valid item is added to the cart
                    elif quantity > 0:
                        flash(f"We are out of stock on {row[1]}! Try a different quantity.", category="error")
                else:
                    print("length of Cart 1: ", len(cart_items))
                    if len(cart_items) <0:
                        flash("Invalid quantity selected! Try again.", category="error")
            except ValueError:
                if len(cart_items) < 0:
                    print("length of Cart 1: ", len(cart_items))
                    flash("Invalid quantity format! Try again.", category="error")

        if proceed_to_checkout:
            # Update the session with cart items and total price
            session["name"] = current_user_email
            session["cart_items"] = cart_items
            session["total_price"] = total_price
            return redirect(url_for("views.checkout"))

    return render_template("home.html", current_user_email=current_user_email, result=result, total_price=0)





















@views.route("/checkout", methods=["GET"])
@login_required
def checkout():
    current_user_email = session.get("name")
    cart_items = session.get("cart_items")
    total_price = session.get("total_price")

    #total_price = round(total_price, 2)
    
    # Clear the cart items and total price from the session
    # session.pop("cart_items", None)
    # session.pop("total_price", None)
    
    if cart_items is not None:
        return render_template("checkout.html", cart_items=cart_items, total_price=total_price, current_user_email=current_user_email)
    else:
        # Handle the case when cart_items is None
        flash("Your cart is empty.", category="error")
        return redirect(url_for("views.home"))




























def get_product_from_database(product_id):
    with my_connection.cursor(buffered=True) as db_cursor:
        db_query = "SELECT * FROM products WHERE product_id = %s"
        db_cursor.execute(db_query, (product_id,))
        product = db_cursor.fetchone()
        if product:
            product_data = {
                "product_id": product[0],
                "product_name": product[1],
                "product_quantity": product[2],
                "product_price": product[3]
            }
            return product_data
        return None


def update_order_in_database(product_id, quantity):
    with my_connection.cursor(buffered=True) as db_cursor:
        db_query = "UPDATE products SET product_quantity = product_quantity - %s WHERE product_id = %s"
        db_cursor.execute(db_query, (quantity, product_id))
        my_connection.commit()

@views.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    current_user_email = current_user.id

    if request.method == 'POST':
        # Process the form submission
        # Retrieve the selected product quantities from the form and update the cart

        # Redirect to the cart page to display the updated cart
        return redirect(url_for('views.cart'))

    else:
        cart_items = []
        total_price = 0

        with my_connection.cursor(buffered=True) as db_cursor:
            db_cursor.execute("SELECT * FROM products")
            result = db_cursor.fetchall()

        for row in result:
            product_id = row[0]
            quantity = int(request.form.get(f"quantity_{product_id}", 0))  # Default to 0 if quantity is not provided

            if quantity > 0:
                product = get_product_from_database(product_id)

                if product is not None and product["product_quantity"] >= quantity:
                    item_price = product["product_price"] * quantity
                    total_price += item_price

                    cart_item = {
                        "product_name": product["product_name"],
                        "quantity": quantity,
                        "price": product["product_price"],
                        "total": item_price
                    }
                    cart_items.append(cart_item)

        return render_template("cart.html", current_user_email=current_user_email, cart_items=cart_items, total_price=total_price)


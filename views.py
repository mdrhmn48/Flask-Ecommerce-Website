from flask import Blueprint, render_template, request, redirect, url_for
from product_database import get_products, get_product_categories
from flask_login import  login_required, login_user, current_user
from product_database import my_connection

views = Blueprint("views", __name__)

db_cursor = my_connection.cursor(buffered=True)
dict_list = []
stmt = f'''Select product_name, product_quantity, product_price, category_name
                    from products
	                    join product_categories on products.category_id = product_categories.category_id
                where category_name = "Grains"'''
db_cursor.execute(stmt)
result_set = db_cursor.fetchall()
print(result_set)
for row in result_set: 
        row_dict = {
            "name" : row[0],
            "quantity" : row[1],
            "price" : row[2],
            "category" : row[3]
        }
#out = [item for t in user for item in t]  

@views.route("/", methods= ["GET", "POST"])
# @login_required
def home():
    product = request.form.get("product")
    print(product)
    quantity = request.form.get("quantity")
    if request.method == 'POST':
        if request.form['product'] == 'Rice' or "Cereals":
            print("Helllo")
        elif request.form['product'] == 'Quinoa':
            print("Quinoa")

        else:
            pass # unknown
    for product in result_set:
        print(product)
        # return redirect(url_for('home.submit')) 
    else:
        pass




    return render_template("home.html", title = 'Home', result=get_products("Grains"), prod_cat=get_product_categories(), currentUser=current_user)




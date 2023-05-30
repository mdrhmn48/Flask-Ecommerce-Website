from mysql import connector

my_connection = connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "grocery"
)

db_cursor = my_connection.cursor()

def get_products(category):
    if (not isinstance(category, str)):
        raise ValueError("Category is not a string")
    dict_list = []
    stmt = f'''Select product_name, product_quantity, product_price, category_name
                    from products
	                    join product_categories on products.category_id = product_categories.category_id
                where category_name = "{category}"'''
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set: 
        row_dict = {
            "name" : row[0],
            "quantity" : row[1],
            "price" : row[2],
            "category" : row[3]
        }
        dict_list.append(row_dict)
    return dict_list

# Return all the category names
def get_product_categories():
    cat_list = []
    stmt = "Select * from product_categories"
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set:
        cat_list.append(row)
    return cat_list

def buy_product(email, product_id, quantity_taken, unit_price):
    if (not isinstance(email, str)):
        raise ValueError("Email is not a string")
    if (not isinstance(product_id, int)):
        raise ValueError("Product ID is not a number")
    if (not isinstance(quantity_taken, int)):
        raise ValueError("Quantity is not a number")
    total_purchase_amount = unit_price * quantity_taken
    stmt = f'''
    INSERT INTO customer_products(customer_id, product_id, quantity_taken, total_purchase_amount)
    VALUES ((Select customer_id from Customers where email = "{email}"), 
		(Select product_id from Products where product_id = {product_id}),
        ({quantity_taken}),
        ({total_purchase_amount})
        )
    '''
    db_cursor.execute(stmt)
    my_connection.commit()
    update_quantity(quantity_taken, product_id)

def create_user(first_name, email, password):
    if (not isinstance(first_name, str)):
        raise ValueError("First_name is not a string")
    if (not isinstance(email, str)):
        raise ValueError("Email is not a string")
    if (not isinstance(password, str)):
        raise ValueError("Password is not a string")
    stmt = f'''
    INSERT into customers(first_name, email, customer_pass)
        values("{first_name}", "{email}", "{password}")
        '''
    db_cursor.execute(stmt)
    my_connection.commit()
    print(f"First Name: {first_name}")
    print(f"Email: {email}")

def view_owned_products(email):
    if (not isinstance(email, str)):
        raise ValueError("Email is not a string")
    own_list = []
    stmt = f'''
        SELECT DISTINCT product_name 
        FROM customer_products
        JOIN products ON products.product_id = customer_products.product_id
        WHERE customer_id = (SELECT customer_id FROM customers WHERE email = "{email}")
    '''
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set:
        own_list.append(row[0])
    return own_list

def create_user_review(email, product, star_num):
    if (not isinstance(email, str)):
        raise ValueError("Email is not a string")
    if (not isinstance(product, str)):
        raise ValueError("Product is not a string")
    if (not isinstance(star_num, int)):
        raise ValueError("Star Rating is not a number")
    stmt = f'''
    INSERT INTO Product_reviews(num_stars, product_id)
        Values ({star_num}, (Select product_id from products where product_name = '{product}')); '''
    db_cursor.execute(stmt)

    stmt = f'''
    INSERT INTO customer_product_review(customer_id, product_review_id)
        values((Select customer_id from Customers where email = "{email}"), (SELECT last_insert_id())); '''
    
    db_cursor.execute(stmt)
    my_connection.commit()

def update_quantity(amount_taken, product_id):
    if (not isinstance(amount_taken, int)):
        raise ValueError("The Amount Taken is not a int")
    if (not isinstance(product_id, int)):
        raise ValueError("Product is not a string")
    stmt = f'''Select Product_quantity from Products WHERE product_id = "{product_id}";'''
    db_cursor.execute(stmt)
    current = db_cursor.fetchall()[0][0]
    if (current < amount_taken):
        raise ValueError("Taking more than currently available")
    
    stmt = f'''
    UPDATE products
    SET product_quantity = product_quantity - {amount_taken}
    WHERE product_id = "{product_id}";
    '''
    db_cursor.execute(stmt)
    my_connection.commit()

# [0] = Product Name
# [1] = Category Name / Price
def get_all_products(order_by='product_id'):
    # if not isinstance(order_by, str):
    #     raise ValueError("Order By is not a string")
    # if order_by != 'category' or order_by != 'price':
    #     raise Exception("You can only order by category (default param) or price")
    product_list = []
    if (order_by == 'product_id'):
        stmt = f'''
        SELECT product_id, product_name, category_name, product_price
        from products
        JOIN product_categories
            ON products.category_id = product_categories.category_id
        ORDER BY product_id;
        '''

    elif (order_by == 'category'):
        stmt = f'''
                SELECT product_id, product_name, category_name, product_price
                from products
                JOIN product_categories
                    ON products.category_id = product_categories.category_id
                ORDER BY category_name;
        '''
    elif (order_by == 'price'):
        stmt = f'''
        SELECT product_name, product_price, category_name
        FROM products
        ORDER BY product_price DESC;
        '''
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set:
        product_list.append(row)
    return result_set

#Star ratings = pop
def get_reviews_by_pop():
    pop_list = []
    stmt = f'''
    SELECT first_name, num_stars, product_name 
    FROM product_reviews
	    JOIN products on products.product_id = product_reviews.product_id
	    JOIN customer_product_review on customer_product_review.product_review_id = product_reviews.product_review_id
	    JOIN customers on customers.customer_id = customer_product_review.customer_id
    Order by num_stars;
    '''
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set:
        pop_list.append(row)
    return result_set

def delete_user(email):
    if (not isinstance(email, str)):
        raise ValueError("Email is not a string")
    stmt = f'''
    DELETE FROM customers
    WHERE email = '{email}';
    '''
    db_cursor.execute(stmt)
    my_connection.commit()

# Valid categories: Fruits, Vegetables, Snacks, Grains, Meat, Dairy
def add_fruit(product_name, quantity, price, category):
    if (not isinstance(product_name, str)):
        raise ValueError("Product Name is not a string")
    if (not isinstance(quantity, int)):
        raise ValueError("Quantity is not an int")
    if (not isinstance(price, float)):
        raise ValueError("Price is not a float")
    if (not isinstance(category, str)):
        raise ValueError("Category is not a string")
    stmt = f'''
    INSERT INTO Products(product_name, product_quantity, product_price, category_id)
    Values ("{product_name}", {quantity}, {price}, (Select category_id from Product_categories where category_name = "{category}"));
    '''
    db_cursor.execute(stmt)
    my_connection.commit()

# Sorts items by price
def sort_by_price():
    sql = """SELECT product_name, product_price FROM Products ORDER BY product_price"""
    db_cursor.execute(sql)
    price_db = db_cursor.fetchall()
    print(price_db)

# Sorts items by category
def sort_by_category():
    sql = """SELECT p.product_name, pc.category_name FROM Product_categories pc JOIN Products p on pc.category_id = p.category_id ORDER BY category_name"""
    db_cursor.execute(sql)
    category_db = db_cursor.fetchall()
    print(category_db)

# Sorts items by popularity
def sort_by_popularity():
    sql = """SELECT p.product_name, pr.num_stars FROM Product_reviews pr JOIN Products p on pr.product_id = p.product_id ORDER BY num_stars DESC"""
    db_cursor.execute(sql)
    pop_db = db_cursor.fetchall()
    print(pop_db)

# Custom queries/sorts
def custom_query(attributes: list):
    while(True): # reruns until you make a select statement
        custom_query = input(f"Type 1 to sort values by an attribute or 2 to search with a conditional statement: ")
        if custom_query not in ("1", "2"): # makes sure input is 1 or 2
            print("Please type 1 or 2.")
        elif custom_query == "1": # decide to sort by attribute
            while(True):
                attribute = input(f"What attribute do you want to sort by? Choose from this list: ({attributes})\n")
                if attribute not in attributes: # makes sure attribute is in attribute list
                    print("That attribute is not in the table!")
                else:
                    while(True):
                        asc = input("Type 1 to sort in ascending order or 2 to sort in descending order: ")
                        if asc not in ("1", "2"): # makes sure input is 1 or 2
                            print("Please type 1 or 2.")
                        elif asc == "1": # sort products by attribute in ascending order
                            sql = f"SELECT * FROM Products ORDER BY {attribute}"
                            db_cursor.execute(sql)
                            cust_db = db_cursor.fetchall()
                            print(cust_db)
                            break
                        elif asc == "2": # sort products by attribute in descending order
                            sql = f"SELECT * FROM Products ORDER BY {attribute} DESC"
                            db_cursor.execute(sql)
                            cust_db = db_cursor.fetchall()
                            print(cust_db)
                            break
                    break
        elif custom_query == "2": # decide to sort with a conditional statement
            while(True):
                attribute = input(f"What attribute do you want to set a condition for? Choose from this list: ({attributes})\n")
                if attribute not in attributes: # makes sure attribute is in attribute list
                    print("That attribute is not in the table!")
                else:
                    while True:
                        op = input("What operator (>, <, or =) do you want to use: ")
                        if op not in (">", "<", "=", "!="): # makes sure operator is >, <, =, or !=
                            print("Please type either a '>', '<', '=', or '!=' character.")
                        elif op in (">", "<", "=", "!="): # gets value to compare against
                            value = input(f"Enter a value (Put strings in quotes). Only products where {attribute} is {op} the value will be shown: ")
                            try:
                                sql = f"SELECT * FROM Products WHERE {attribute} {op} {value}"
                                print(f"SQL: {sql}")
                                db_cursor.execute(sql)
                                cust_db = db_cursor.fetchall()
                                print(cust_db)
                                break
                            except Exception as e:
                                print(f"Error: {e}")
                                break
                    break
        break

def view_all_orders(customer_id):
    customer_id = customer_id
    order_list = []
    stmt = f'''
            SELECT customer_products.order_id, products.product_name, customer_products.quantity_taken, 
            customer_products.total_purchase_amount from customer_products
            JOIN products ON customer_products.product_id = products.product_id
            WHERE customer_id = "{customer_id}"
            ORDER BY order_id;
            '''
    
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set:
        order_list.append(row)
    return result_set

def view_total_purchase_amount(customer_id):
    customer_id=customer_id
    total_purchase_amount = []
    stmt = f'''
            SELECT ROUND(SUM(total_purchase_amount),2) from customer_products
            WHERE customer_id = "{customer_id}";
            '''
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set:
        total_purchase_amount.append(row)
    return result_set
    
def view_purchased_products(customer_id):
    product_list = []
    stmt = f"""
            SELECT products.product_name from customer_products
            JOIN products ON customer_products.product_id = products.product_id
            WHERE customer_id = {customer_id}
            ORDER BY order_id;
            """
    db_cursor.execute(stmt)
    result_set = db_cursor.fetchall()
    for row in result_set:
        product_list.append(row)
    return result_set

if (__name__ == "__main__"):
    custom_query(["product_id", "product_name", "product_quantity", "product_price", "category_id"])

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

def buy_product(email, product_name, quantity_taken):
    if (not isinstance(email, str)):
        raise ValueError("Email is not a string")
    if (not isinstance(product_name, str)):
        raise ValueError("Product Name is not a string")
    if (not isinstance(quantity_taken, int)):
        raise ValueError("Quantity is not a number")
    stmt = f'''
    INSERT INTO customer_products(customer_id, product_id)
    VALUES ((Select customer_id from Customers where email = "{email}"), 
		(Select product_id from Products where product_name = "{product_name}"))
    '''
    db_cursor.execute(stmt)
    my_connection.commit()
    update_quantity(quantity_taken, product_name)

def create_user(email, first_name, password):
    if (not isinstance(email, str)):
        raise ValueError("Email is not a string")
    if (not isinstance(first_name, str)):
        raise ValueError("First_name is not a string")
    if (not isinstance(password, str)):
        raise ValueError("Password is not a string")
    stmt = f'''
    INSERT into customers(email, first_name, customer_pass)
        values("{email}", "{first_name}", "{password}")
    '''
    db_cursor.execute(stmt)
    my_connection.commit()

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

def update_quantity(amount_taken, product):
    if (not isinstance(amount_taken, int)):
        raise ValueError("The Amount Taken is not a int")
    if (not isinstance(product, int)):
        raise ValueError("Product is not a string")
    stmt = f'''Select Product_quantity from Products WHERE product_name = "{product}";'''
    db_cursor.execute(stmt)
    current = db_cursor.fetchall()[0][0]
    if (current < amount_taken):
        raise ValueError("Taking more than currently available")
    
    stmt = f'''
    UPDATE products
    SET product_quantity = product_quantity - {amount_taken}
    WHERE product_name = "{product}";
    '''
    db_cursor.execute(stmt)
    my_connection.commit()

# [0] = Product Name
# [1] = Category Name / Price
def get_all_products(order_by='category'):
    if (not isinstance(order_by, str)):
        raise ValueError("Order By is not a string")
    if (order_by is not 'category' or order_by is not 'price'):
        raise Exception("You can only order by category (default param) or price")
    product_list = []
    if (order_by == 'category'):
        stmt = f'''
        SELECT product_name, category_name
        from products
        JOIN product_categories
            ON products.category_id = product_categories.category_id
        ORDER BY category_name;
        '''
    elif (order_by == 'price'):
        stmt = f'''
        SELECT product_name, product_price
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


if (__name__ == "__main__"):
    print(get_all_products("Testing"))

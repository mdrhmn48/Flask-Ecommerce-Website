from database_source_files.product_database import *

db_curser = my_connection.cursor()

print("Welcome to our Grocery Store!")
def create_account():
    while True:
        create_account = input("Would you like to create an account?Y/N: ")
        create_account = create_account.lower()
        if(create_account != "y"):
            break
        else:
            first_name = input("What is first name: ")
            email=input("What is your email?: ")
            password=input("What is your password?: ")
            print(create_user(first_name, email, password))
            print("Account created")
        # print(create_user())
        
def view_account():
        # db_cursor.execute("""select first_name from customers""")
        # first_name = db_cursor.fetchall()
        # first_name = [item for t in first_name for item in t]
        email=input("Which email/account would you like to view?: ")
        db_cursor.execute("""select email, customer_id from customers""")
        email_db = db_cursor.fetchall()
        customer_id = int(email_db[0][1])
        print(email_db)
        email_db = [item for t in email_db for item in t] 
        print(email_db)
        db_cursor.execute("""select customer_pass from customers""")
        password = db_cursor.fetchall()
        print(password)
        password_db = [item for t in password for item in t]
        print(password_db)
          
        if email in email_db:
            password= input("What is your password? ")
            # if password in password_db:
            if password in password_db:
                    print("\n------------------------------")
                    print("\nSelect an option?")
                    print("\nOption 1: View all order numbers")
                    print("\nOption 2: View total purchase price of all orders")
                    print("\nOption 3: View list of individual purchased products")
                    print("\n------------------------------")
                    
                    choice = int(input("Please select an option: "))
                    if choice == 1:
                        print("\nList of all order numbers:")
                        orders_list = view_all_orders(customer_id=customer_id)
                        for i in orders_list:
                            print(i)
                    
                    elif choice == 2:
                        print("\nTotal Purchase Price of All Orders (in dollars):")
                        purchase_price_list = view_total_purchase_amount(customer_id=customer_id)
                        print(f"${purchase_price_list[0][0]}")

                    elif choice == 3:
                        print("\nList of purchased products:")
                        purchased_products = view_purchased_products(customer_id=customer_id)
                        product_list = map(lambda x: x[0], purchased_products)
                        for i in product_list:
                            print(i)
                        # pass
                    else:
                        print("Thank you for visiting")
            else:
                print("Wrong Password! Try Again")
        else:
            print("Email do not exist!")

def update_account():
    while True:
        update_account = input("Would you like to update an account?Y/N: ")
        update_account = update_account.lower()
        if(update_account[0] != "y"):
            return
        else:
            break
    while True:
        email=input("Which email would you like to update?: ")
        db_cursor.execute("""select email from customers""")
        email_input = db_cursor.fetchall()
        print(f"email_input: {email_input}")
        email_db = [item for t in email_input for item in t] 
        print(f"email_db: {email_db}")
        db_cursor.execute("""select customer_pass from customers""")
        password = db_cursor.fetchall()
        print(f"password = {password}")
        password_db = [item for t in password for item in t]
        print(f"password_db = {password_db}")  
        if email in email_db:
            while True:
                password= input("What is your passowrd? ")
                # if password in password_db:
                if password in password_db:
                    while True:
                        update_acc = input("Would you like to update email or password?(email/password)")
                        update = update_acc[0].lower()
                        if (update != "e") and (update != "p"):
                            print("Please Enter Either email or Password to update: ")
                            continue
                        else:
                            print(f"You picked {update_acc}")
                            # enter the new information
                            new_update = input(f"Enter your new {update_acc}: ")
                            print(f"input: {new_update}")
                            if update_acc == 'email':
                                old_email = email_db[0]
                                sql_statement = f"Update customers set email = '{new_update}' where email = '{old_email}'"
                                db_curser.execute(f"""{sql_statement}""")
                                my_connection.commit()
                            if update_acc == 'password':
                                old_password = password_db[0]
                                sql_statement = f"Update customers set customer_pass = '{new_update}' where customer_pass = '{old_password}'"
                                db_curser.execute(f"""{sql_statement}""")
                                my_connection.commit()
                            return
                else:
                    print("Wrong Password! Try Again")
        else:
            print("Email do not exist!")

def delete_account():
    while True:
        delete_account = input("Would you like to delete an account?Y/N: ")
        delete_account = delete_account.lower()
        if(delete_account[0] != "y"):
            return
        else:
            break
    while True:
        email=input("Which email would you like to delete?: ")
        db_cursor.execute("""select email from customers""")
        email_db = db_cursor.fetchall()
        print(email_db)
        email_db = [item for t in email_db for item in t] 
        print(email_db)
        db_cursor.execute("""select customer_pass from customers""")
        password = db_cursor.fetchall()
        print(password)
        password_db = [item for t in password for item in t]
        print(password_db)  
        if email in email_db:
            while True:
                password= input("What is your password? ")
                # if password in password_db:
                if password in password_db:
                        delete_user(email)
                        print(f"{email} been deleted")
                        print("Thank you for shopping")  
                        return
                else:
                    print("Wrong Password! Try Again")
        else:
            print("Email do not exist!")
      
            
def buy():
    email=input("Enter the email address for your account: ")
    db_cursor.execute(f"""select email from customers where email = '{email}'""")
    email_input = db_cursor.fetchall()
    print(f"email_input: {email_input}")
    email_db = [item for t in email_input for item in t] 
    print(f"email_db: {email_db}")
    password=input("Enter the password for your account: ")
    db_cursor.execute(f"""select customer_pass from customers where customer_pass = '{password}'""")
    password_input = db_cursor.fetchall()
    print(f"password = {password_input}")
    password_db = [item for t in password_input for item in t]
    print(f"password_db = {password_db}")

    if email in email_db:
        print("\n------------------------------")
        print("\nList of available products")
        print("\n------------------------------")
        product_list = get_all_products()
        for x in range(len(product_list)):
            print(product_list[x])
        print("\n------------------------------")
        product_id=input("Enter selection number of the product you wish to purchase: ")
        product_id=int(product_id)
        db_cursor.execute(f"""Select product_name from products WHERE product_id = '{product_id}'""")
        product_pick = db_cursor.fetchall()
        product_selection = str(product_pick[0][0])
        print(f"You have selected {product_selection}")
        quantity_taken = input(f"Enter quantity of {product_selection}: ")
        quantity_taken=int(quantity_taken)
        db_cursor.execute(f'''Select product_price from products WHERE product_id = "{product_id}"''')
        product_price = db_cursor.fetchall()
        unit_price = float(product_price[0][0])
        buy_product(email=email, product_id=product_id, quantity_taken=quantity_taken, unit_price=unit_price)
        print(f"You have successfully purchased {product_selection}, quantity: {quantity_taken}, unit_price: {unit_price}")
    else:
        print("Account email does not exist")

def review():
    pass
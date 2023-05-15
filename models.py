from product_database import *

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
            create_user(email,first_name, password)
            print("Account created")
            return
        # print(create_user())
def view_account():
    while True:
        view_account = input("Would you like to view your account? Y/N: ")
        view_account = view_account.lower()
        if(view_account[0] != "y"):
            break
        else:
            while True:
                db_cursor.execute("""select first_name from customers""")
                first_name = db_cursor.fetchall()
                first_name = [item for t in first_name for item in t]
                email=input("Which email/account would you like to view?: ")
                db_cursor.execute("""select email from customers""")
                email_db = db_cursor.fetchall()
                # print(email_db)
                email_db = [item for t in email_db for item in t] 
                # print(email_db)
                db_cursor.execute("""select customer_pass from customers""")
                password = db_cursor.fetchall()
                # print(password)
                password_db = [item for t in password for item in t]
                # print(password_db)
          
                if email in email_db:
                        password= input("What is your passowrd? ")
                        # if password in password_db:
                        if password in password_db:
                            while True:
                                print("----------------------------------")
                                # while True:
                                print("\nOption 1: Update your account")
                                print("\nOption 2: Buy a product")
                                print("\nOption 3: Leave a review?")
                                print("\nOption 4: Delete your account")
                                print("\n------------------------------")
                                try:
                                    choice = input("Please select an option?")
                                    choice = int(choice)
                                except ValueError:
                                    print("Please input integer only...")
                                    continue
                                if choice == 1:
                                    print(f"Your picked option{choice}")
                                    update_account(email)       
                                elif choice == 2:
                                    print(f"Your picked option{choice}")
                                    #print(get_products("Grains"))
                                    buy_products()
                                    #buy_product(email)
                                    print(f"finished")
                                        # buy()
                                elif choice == 3:
                                    create_user_review(email)
                                elif choice == 4:
                                        while True:
                                            delete_account = input("Are you sure you want delete your account?Y/N: ")
                                            delete_account = delete_account.lower()
                                            if(delete_account[0] != "y"):
                                                break
                                            else:
                                                delete_user(email)
                                                print(f"{email} been deleted")
                                                print("Thank you for shopping")
                                                #delete_account()
                                                return
                                else:
                                    break
                                    # print("Error")
                        else:
                            print("Wrong Password! Try Again")
                else:
                    print("Email do not exist!")

                    

def update_account(email):
    while True:
        update_account = input("Would you like to update an account?Y/N: ")
        update_account = update_account.lower()
        if(update_account[0] != "y"):
            return
        else:
            break
    while True:
            update_acc = input("Would you like to update email or password?(email/customer_pass)")
            update = update_acc[0].lower()
            if (update != "e") and (update != "c"):
                print("Please Enter Either email or Password to update: ")
                continue
            else:
                print(f"You picked {update_acc}")
                # enter the new information
                new_update = input(f"Enter your new {update_acc}: ")
                db_curser.execute(f"""UPDATE customers set {update_acc} = "{new_update}" where email="{email}";""")
                my_connection.commit()
                print(f"Your new {update_acc} is: {new_update}")
                print(f"Its been updated. Thank you!")
                return
        

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
        # print(email_db)
        email_db = [item for t in email_db for item in t] 
        # print(email_db)
        db_cursor.execute("""select customer_pass from customers""")
        password = db_cursor.fetchall()
        # print(password)
        password_db = [item for t in password for item in t]
        print(password_db)  
        if email in email_db:
            while True:
                password= input("What is your passowrd? ")
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
      
    
def buy_products():
    dict_list = []
    db_curser.execute(f'''Select product_name, product_quantity, product_price
                    from products''')
    result_set = db_curser.fetchall()
    # print(result_set)
    for i, tup in enumerate(result_set):
        print(f"{i}\t{tup}")
    # return
    #  row_dict = {
    #         "product_name" : row[0],
    #         "quantity" : row[1],
    #         "price" : row[2],
    #         # "category" : row[3]
    #     }
    # for row in result_set:
   
    while True:
        try:
            selected_product_index = int(input("Select a product to buy? (index)"))
            if selected_product_index >=0 and selected_product_index < len(result_set):
                pass
            else:
                print(f"Index shoud be less than {len(result_set)} and greater than equal to 0.")
                continue
        except:
            print("Index could not be string")
            continue
        print(f"You select {result_set[selected_product_index]}")
        break
        # if selected_product in row[0]:
    while True:
        try:
            quantity = input("What's the quantity you would like to buy? ")
            quantity = int(quantity)
            if (quantity < 0) or  (quantity> result_set[selected_product_index][1]):
                print(f"Quantity must be greater than or equal to 0 or less than or equal to {result_set[selected_product_index][1]}")
                continue
            # elif  (quantity >= 0) and  (quantity < result_set[selected_product_index][1]):
            else:
                total = quantity * result_set[selected_product_index][2]
                print(f"Your total: {total}")
                stmt = f'''UPDATE products SET product_quantity = product_quantity - {quantity}
                WHERE product_name = "{result_set[selected_product_index][0]}";'''
                db_cursor.execute(stmt)
                my_connection.commit()
                return
        except ValueError:
            print("Please input integer only...")
            continue      
        # else:
        #     print("Please type a product from the list")
        #     continue
        #select product_quantity from products where product_name = row{1}

def create_user_review(email):
    dict_list = []
    db_curser.execute(f'''Select product_name, product_quantity, product_price
                    from products''')
    result_set = db_curser.fetchall()
    for i, tup in enumerate(result_set):
        print(f"{i}\t{tup}")
        
    while True:
        try:
            selected_product_index = int(input("Select a product to review? (index)"))
            if selected_product_index >=0 and selected_product_index < len(result_set):
                pass
            else:
                print(f"Index shoud be less than {len(result_set)} and greater than equal to 0.")
                continue
        except:
            print("Index could not be string")
            continue
        print(f"You select {result_set[selected_product_index]}")
        break
        # if selected_product in row[0]:
    while True:
        try:
            rating = input("Enter a number between 0-10 for review? ")
            rating = int(rating)
            if rating > 10 or rating < 1:
                print(f"rating must be between 1-10")
                continue
            else: 
                print(f"Your gave: {rating} Star")
                stmt = f'''
                INSERT INTO Product_reviews(num_stars, product_id)
                    Values ({rating}, (Select product_id from products where product_name = '{result_set[selected_product_index][0]}')); '''
                db_cursor.execute(stmt)
                stmt = f'''
                INSERT INTO customer_product_review(customer_id, product_review_id)
                    values((Select customer_id from Customers where email = "{email}"), (SELECT last_insert_id())); '''
                
                db_cursor.execute(stmt)
                my_connection.commit()
                return
        except ValueError:
                print("Please input integer only...")
                continue   
    

                        
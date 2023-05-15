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
            print(create_user(first_name, email, password))
            print("Account created")
        # print(create_user())
def view_account():
    while True:
        view_account = input("Would you like to view your account? Y/N: ")
        view_account = view_account.lower()
        if(view_account[0] != "y"):
            return
        else:
            break
    while True:
        # db_cursor.execute("""select first_name from customers""")
        # first_name = db_cursor.fetchall()
        # first_name = [item for t in first_name for item in t]
        email=input("Which email/account would you like to view?: ")
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
                password= input("What is your passowrd? ")
                # if password in password_db:
                if password in password_db:
                        print(f"Your email: {email}")
                        print("Thank you for shopping")  
                        break
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
                            new_update = input("Enter your {update_acc}")
                            db_curser.execute("""select customers set {}""")
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
      
    
            
def buy():
    pass
def review():
    pass
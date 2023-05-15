from website import create_app
from website import models as store

app = create_app()

if __name__== "__main__":
    app.run(debug=True)

# while True:
#         print("\nWelcome to Grocery Store!")
#         print("\nSelect an 1 to create, 2 to login and any other interger to quit?")
#         print("\nOption 1: Create an account? ")
#         print("\nOption 2: View your account")
#         print("\n------------------------------")
#         try:
#                 choice = input("Please select an option?")
#                 choice = int(choice)
#         except ValueError:
#                 print("Please input integer only...") 
#                 continue
#         if choice == 1:
#                 store.create_account()        
#         elif choice == 2:
#                 store.view_account()
#         else:
#                 print("Thank you for visiting")
#                 break
        


from website import create_app
from website import models as store
from database_source_files import product_database as pdb

app = create_app()
while True:
    print("\nWelcome to Grocery Store!")
    print("\nSelect an option?")
    print("\nOption 1: Create an account? ")
    print("\nOption 2: View your account")
    print("\nOption 3: Update your account")
    print("\nOption 4: Delete your account")
    print("\nOption 5: Buy?")
    print("\nOption 6: Sort products")
    print("\n------------------------------")

    choice = int(input("Please select an option: "))
    if choice == 1:
            store.create_account()
            pass
    elif choice == 2:
            store.view_account()
            pass
    elif choice == 3:
            store.update_account()
            pass
    elif choice == 4:
            store.delete_account()
    elif choice == 5:
            store.buy()
            pass
    elif choice == 6:
            print("\nOption 1: Sort by price")
            print("\nOption 2: Sort by popularity")
            print("\nOption 3: Sort by category")
            print("\nOption 4: Custom query")
            print("\n------------------------------")
            choice2 = int(input("Please select an option: "))
            if choice2 == 1:
                print("Here is a list with the product name and price of all items: ")
                pdb.sort_by_price()
                pass
            elif choice2 == 2:
                print("Here is a list with the product name and number of stars for all reviewed items: ")
                pdb.sort_by_popularity()
                pass
            elif choice2 == 3:
                print("Here is a list with the product name and category for all items: ")
                pdb.sort_by_category()
                pass
            elif choice2 == 4:
                print("Results will be in format: product_id, product_name, product_quantity, product_price, category_id")
                pdb.custom_query(["product_id", "product_name", "product_quantity", "product_price", "category_id"]) # list of valid attributes
                pass
    else:
            print("Thank you for visiting")
            break
        
# store.create_account()
#store.read_account()
# store.delete_account()=

if __name__== "__main__":
    app.run(debug=True)
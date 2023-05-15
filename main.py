from website import create_app
from website import models as store

app = create_app()
while True:
    print("\nWelcome to Grocery Store!")
    print("\nSelect an option?")
    print("\nOption 1: Create an account? ")
    print("\nOption 2: View your account")
    print("\nOption 3: Update your account")
    print("\nOption 4: Delete your account")
    print("\nOption 5: Buy?")
    print("\nOption 6: Review your products")
    print("\n------------------------------")

    
    choice = int(input("Please select an option?"))
    if choice == 1:
            # store.create_account()
            pass
    elif choice == 2:
            store.view_account()
            pass
    elif choice == 3:
            # store.update_account()
            pass
    elif choice == 4:
            store.delete_account()
    elif choice == 5:
            # store.buy()
            pass
    elif choice == 6:
            # store.review()
            pass
    else:
            print("Thank you for visiting")
            break
        

# store.create_account()
#store.read_account()
# store.delete_account()


if __name__== "__main__":
    app.run(debug=True)
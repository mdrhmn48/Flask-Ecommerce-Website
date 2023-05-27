This project is a Flask application that implements user authentication and user profile functionality. It uses the Flask framework, MySQL database, and Flask-Login extension for managing user sessions.

    Install the necessary dependencies by running the following command:

pip install flask flask-login mysql-connector-python bcrypt

Set up the MySQL database and update the product_database.py file with your database credentials.

Run the Flask application using the following command:

  flask run

Files

   product_database.py: Contains the MySQL database connection setup.
   auth.py: Defines the authentication blueprint, which handles login, registration, and profile update functionalities.
   user.py: Defines the User class used for user authentication and session management.
   views.py: Contains other views/routes of the application.

Functionality
Login

    URL: /login
    Method: GET, POST
    Renders the login page and handles form submission for user authentication.
    If the provided email exists and the password is correct, the user is logged in and redirected to the home page.
    If the email or password is incorrect, an error message is displayed.

Logout

    URL: /logout
    Method: GET
    Logs out the currently authenticated user and redirects to the login page.

Sign-up

    URL: /sign-up
    Method: GET, POST
    Renders the sign-up page and handles form submission for user registration.
    Validates the input fields and creates a new user in the database if all conditions are met.
    Displays appropriate error messages if any validations fail.

Profile

    URL: /profile
    Method: GET, POST
    Renders the user profile page and handles form submission for updating the user's profile information.
    Validates the input fields and updates the user's first name in the database if all conditions are met.
    Displays appropriate error messages if any validations fail.

Database Structure

The project assumes the existence of a MySQL database with the following table:

    Table name: customers
    Columns: email, first_name, customer_pass

The email column stores the user's email address (unique), first_name stores the user's first name, and customer_pass stores the hashed password.
Credits

This project was developed using Flask, Flask-Login, and MySQL.

from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from database_source_files.product_database import my_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from flask_login import UserMixin, LoginManager


currentUser = ""
auth = Blueprint("auth", __name__)

db_cursor = my_connection.cursor(buffered=True)
db_cursor.execute("""SELECT email, customer_pass FROM customers""")
user_rows = db_cursor.fetchall()
user_dict = {row[0].lower(): row[1] for row in user_rows}


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@auth.route("/login", methods=["GET", "POST"])
def login():
    db_cursor.execute("""SELECT email, customer_pass FROM customers""")
    user_rows = db_cursor.fetchall()
    user_dict = {row[0].lower(): row[1] for row in user_rows}

    print("Emails in database:", user_dict)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(f"Input email: {email}")
        print(f"Input password: {password}")
        print("User dictionary:", user_dict)
       

        if email.lower() in user_dict:
            hashed_password = user_dict[email.lower()]

            if check_password_hash(hashed_password, password):
                global currentUser
                currentUser = email
                flash(f"{currentUser} logged in successfully!", category="success")

                user = UserMixin()
                user.id = email  # Set the user ID
                login_user(user, remember=True)


                #login_user(current_user, remember=True)
                return redirect(url_for('views.home'))  
            else:
                flash("Incorrect Password. Try again!", category="error")
                print(f"Input password: {password}")
                print(f"Hashed password from database: {hashed_password}")
        else:
            flash("Email does not exist!", category="error")
            print(f"Input email: {email}")
            print("Emails in database:", user_dict)
    return render_template("login.html", currentUser=current_user)


@auth.route("/logout")
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if email in user_dict:
            flash("Email already exists!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(firstName) < 2:
            flash("First name must be greater than 1 character", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 7:
            flash("Password too short. Must be greater than 6 characters", category="error")
        else:
            hashed_password = generate_password_hash(password1)
            db_cursor.execute("INSERT INTO customers(email, first_name, customer_pass) VALUES (%s, %s, %s)", (email, firstName, hashed_password))
            my_connection.commit()
            # db_cursor.execute("""SELECT email, customer_pass FROM customers""")
            # db_cursor.fetchall()
            

            # print("Emails in databasess:", user_dict)
            flash("Account created successfully", category="success")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", currentUser=current_user)


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    #session.pop('username', None)
    #showProfile()
    return render_template("profile.html", currentUser=current_user)
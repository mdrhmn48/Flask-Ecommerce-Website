from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from database_source_files.product_database import my_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from flask_login import UserMixin, LoginManager



currentUser = ""
auth = Blueprint("auth", __name__)

db_connection = my_connection
db_cursor = my_connection.cursor(buffered=True)
db_cursor.execute("""SELECT email, customer_pass FROM customers""")
user_rows = db_cursor.fetchall()
user_dict = {row[0].lower(): row[1] for row in user_rows}


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    db_cursor = db_connection.cursor(buffered=True)
    db_cursor.execute("SELECT email FROM customers WHERE email = %s", (user_id,))
    result = db_cursor.fetchone()
    print("user_id: ", result[0])
    db_cursor.close()
    if result:
        return User(result[0])
    else:
        return None
    

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # db_cursor = db_connection.cursor(buffered=True)
        db_cursor.execute("SELECT email, customer_pass FROM customers WHERE email = %s", (email,))
        result = db_cursor.fetchone()
        # db_cursor.close()

        if result:
            hashed_password = result[1]
            if check_password_hash(hashed_password, password):
                user = User(result[0])
                login_user(user, remember=True)
                flash(f"{current_user.id} logged in successfully!", category="success")
                session["email"] = email
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password. Try again!", category="error")
        else:
            flash("Email does not exist!", category="error")
    return render_template("login.html", currentUser=current_user)

@auth.route("/logout")
@login_required
def logout():
    session.pop('email', None)
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
            db_cursor.execute("INSERT INTO customers(email, first_name, customer_pass) VALUES (%s, %s, %s)", (email, firstName, hashed_password)),
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
    
    flash(f"{current_user.id} logged in successfully!", category="success")
    return render_template("profile.html", currentUser=current_user)
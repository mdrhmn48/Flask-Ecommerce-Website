from flask import Blueprint, render_template, request, flash, redirect, url_for
from product_database import my_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

currentUser = ""
auth = Blueprint("auth", __name__)

db_cursor = my_connection.cursor(buffered=True)
db_cursor.execute("""select email from customers""")
user = db_cursor.fetchall()
out = [item for t in user for item in t]      
print(out)


db_cursor.execute("""select customer_pass from customers""")
password = db_cursor.fetchall()
passwordd = [item for t in password for item in t]      
print(passwordd)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email in out:
            global currentUser
            currentUser = email
            if password in passwordd:
            # if check_password_hash(passwordd, password):
                # email = email.split("")
                flash(f"{currentUser} logged in successfully!", category="success")
                # login_user(user, remember=True)
                login_user(current_user, remember=True)
                return redirect(url_for('views.home'))  
            else:
                flash("Incorrect Password. Try again!", category="error")
        else:
            flash("Email does not Exist!", category="error")
    return render_template("login.html", currentUser= current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up")
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if email in out:
            flash("Email already exist!", category="error")
        elif len(email)<4:
            flash("Email Must be greater than 3 characters", category="error")
        elif len(firstName)<2:
            flash("First name Must be greater than 1 character", category="error")
        elif password1 != password2:
            flash("Password don't match", category="error")
        elif len(password1)<7:
            flash("Password too short. Must be greater than 6 characters", category="error")
        else:
            new_user = db_cursor.execute('''INSERT INTO customers(email,first_name,password) VALUES(%s,%s,%s)''',(email,firstName,password1))
            my_connection.commit()
            login_user(new_user, remember=True)
            flash("Account is created successfully", category="success")
            # login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", currentUser= current_user)
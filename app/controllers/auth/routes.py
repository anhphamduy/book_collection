import re
from flask import render_template, url_for, redirect, request, flash, jsonify, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.controllers.auth import bp
from app.models import User

# login route. User to log the user in
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if len(password) <= 8 and len(username) < 1:
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))

        login_user(user, remember=bool(remember))
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.home")
        return redirect(next_page)
    return render_template("auth/login.html")

# used for registering the user
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return "You are already logged in"
    if request.method == "POST":
        # in case it does not pass all the tests, the values from the form are still saved
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        password1 = request.form.get("password1").strip()
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")

        session["register"] = {
            "username": username,
            "password": password,
            "password1": password1,
            "email": email,
            "firstName": firstName,
            "lastName": lastName
        }
        if User.query.filter_by(username=username).first() is not None:
            flash("Username already exists.")
            return redirect(url_for("auth.register"))
        elif password != password1:
            flash("Password does not match.")
            return redirect(url_for("auth.register"))
        elif len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("auth.register"))
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.")
            return redirect(url_for("auth.register")) 
        # once all validations are successfull
        user = User(email=email, username=username, first_name=firstName.strip().lower(), last_name=lastName.strip().lower())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session.pop("register", None)
        flash("You have successfully registered.")
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for("auth.login"))
    data = session.get("register", None)
    session.pop("register", None)
    return render_template("auth/register.html", data=data) 

# logging out user
@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Successful logging out.")
    return redirect(url_for("auth.login"))

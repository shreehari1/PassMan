from flask import Blueprint, render_template, request, redirect, url_for
from . models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth', '__name__')

@auth.route('/login', methods= [ 'GET','POST'])
def login():
    errorMessages = ""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # check user in DB
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                errorMessages = "Entered Email or Password is wrong"
        else:
            errorMessages = "User does not exist. Please Sign up"
    return render_template("login.html",errormsg=errorMessages, user=current_user)

@auth.route('/totp')
def totp():
    return render_template("totp.html")

@auth.route('/signup', methods= ['GET','POST'])
def signup():
    errorMessages = {
        "field": "",
        "message": ""
    }
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            errorMessages["field"] = "email"
            errorMessages["message"] = "Email already exists"

        elif len(email) < 4:
            errorMessages["field"] = "email"
            errorMessages["message"] = "Email must be greater in length"
        elif len(name) < 4:
            errorMessages["field"] = "name"
            errorMessages["message"] = "Name must be greater in length"
        elif password1 != password2:
            errorMessages["field"] = "password2"
            errorMessages["message"] = "Both password must be same"
        elif len(password1) < 4:
            errorMessages["field"] = "password1"
            errorMessages["message"] = "Password must be greater in length"
        else:
            # add user to DB and logout
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))


    return render_template("sign-up.html", errormsg=errorMessages, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
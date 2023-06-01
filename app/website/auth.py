from flask import Blueprint, render_template, request, flash


auth = Blueprint('auth', '__name__')

@auth.route('/login', methods= [ 'GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # check user in DB
    return render_template("login.html")

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

        if len(email) < 4:
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
            pass

    return render_template("sign-up.html", errormsg=errorMessages)

@auth.route('/logout')
def logout():
    return "<p> Logout page <p>"
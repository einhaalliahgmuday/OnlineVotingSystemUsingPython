from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import models

auth = Blueprint('auth', __name__)

def getUser(userId, password, userType):
    user = models.User.query.filter(models.User.userId == userId, models.User.password == password, models.User.userType == userType).first()
    return user

@auth.route('/login')
def login():
    return render_template('index.html')

@auth.route('/login/admin', methods=['GET', 'POST'])
def loginAdmin():
    if request.method == 'POST':
        user = getUser(request.form.get('userId'), request.form.get('password'), "Admin")
        if user:
            login_user(user)
            return redirect(url_for("views.home"))
        else:
            return "Invalid credentials."

    return render_template("AdminLoginForm.html")

@auth.route('/login/student', methods=['GET', 'POST'])
def loginStudent():
    if request.method == 'POST':
        user = getUser(request.form.get('userId'), request.form.get('password'), "Student")
        if user:
            login_user(user)
            return redirect(url_for("views.home"))
        else:
            return "Invalid credentials."
        # flash('Incorrect password, try again.', category='error')

    return render_template("StudentLoginForm.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()   
    return redirect(url_for('auth.login'))
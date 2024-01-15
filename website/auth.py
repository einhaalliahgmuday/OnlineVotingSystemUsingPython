from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import models

auth = Blueprint('auth', __name__)

def isUserExists(userType, userId, password):
    user = None

    if userType == "student":
        user = models.Student.query.get(userId)
    elif userType == "admin":
        user = models.Admin.query.get(userId)

    if user:
        if user.password == password:
            login_user(user, remember=False)
            return True
                
        else:
            return False
    else:
        return False

@auth.route('/login/admin', methods=['GET', 'POST'])
def loginAdmin():
    if request.method == 'POST':
        if isUserExists("admin", request.form.get('userId'), request.form.get('password')):
            return redirect(url_for("views.home"))
        else:
            return "Invalid credentials."

    return render_template("login-admin.html")  #, user=current_user

@auth.route('/login/student', methods=['GET', 'POST'])
def loginStudent():
    if request.method == 'POST':
        if isUserExists("student", request.form.get('userId'), request.form.get('password')):
            return redirect(url_for("views.home"))
        else:
            return "Invalid credentials."
        # flash('Incorrect password, try again.', category='error')

    return render_template("login-student.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.selectUserType'))
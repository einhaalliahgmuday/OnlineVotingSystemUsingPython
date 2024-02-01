from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import models, rules

auth = Blueprint('auth', __name__)

# MAIN ROUTE WHEN A USER IS NOT LOGGED IN
# RETURNS INDEX.HTML FOR USERS TO SELECT USER TYPE (STUDENT OR ADMIN)
@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    
    return render_template('index.html')

# ROUTE FOR ADMIN LOGIN
@auth.route('/login/admin', methods=['GET', 'POST'])
def loginAdmin():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    
    if request.method == 'POST':
        user = rules.getUser(request.form.get('userId'), request.form.get('password'), "Admin")
        if user:
            login_user(user)
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials.", 'error')

    return render_template("login-admin.html")

# ROUTE FOR STUDENT LOGIN
@auth.route('/login/student', methods=['GET', 'POST'])
def loginStudent():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    
    if request.method == 'POST':
        user = rules.getUser(request.form.get('userId'), request.form.get('password'), "Student")
        if user:
            login_user(user)
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials.", 'error')

    return render_template("login-student.html")

# ROUTE THAT LOGS OUT THE USER; REDIRECTS TO INDEX
@auth.route('/logout')
@login_required
def logout():
    logout_user()   
    return redirect(url_for('auth.login'))
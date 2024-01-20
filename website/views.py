from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
from . import db
from . import models

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/select-user-type')
def selectUserType():
    return render_template('select-user-type.html')

@views.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if request.method == 'POST':
        voter = current_user.userId
        president = request.form.get('president')
        vice_president = request.form.get('vice_president')
        executive_board_sec = request.form.get('executive_board_sec')
        vp_finance = request.form.get('vp_finance')
        vp_academic_affairs = request.form.get('vp_academic_affairs')
        vp_internal_external_affairs = request.form.get('vp_internal_external_affairs')
        vp_public_relations = request.form.get('vp_public_relations')
        vp_research_dev = request.form.get('vp_research_dev')
        first_yr_rep = request.form.get('first_yr_rep')
        second_yr_rep = request.form.get('second_yr_rep')
        third_yr_rep = request.form.get('third_yr_rep')
        fourth_yr_rep = request.form.get('fourth_yr_rep')
          
        if (president == None or vice_president == None or executive_board_sec == None or vp_finance == None or 
            vp_academic_affairs == None or vp_internal_external_affairs == None or vp_public_relations == None or vp_research_dev == None or 
            first_yr_rep == None or second_yr_rep == None or third_yr_rep == None or fourth_yr_rep == None):
            flash('Please fill in all fields.', category="error")
        else:
            vote = models.Vote(voter=voter, president=president, vice_president=vice_president, executive_board_sec=executive_board_sec,
                               vp_finance=vp_finance, vp_academic_affairs=vp_academic_affairs, vp_internal_external_affairs=vp_internal_external_affairs,
                               vp_public_relations=vp_public_relations, vp_research_dev=vp_research_dev, first_yr_rep=first_yr_rep,
                               second_yr_rep=second_yr_rep, third_yr_rep=third_yr_rep, fourth_yr_rep=fourth_yr_rep)
            db.session.add(vote)
            db.session.commit()
            flash('Your vote is counted.', category="success")

    return render_template('vote.html')

    
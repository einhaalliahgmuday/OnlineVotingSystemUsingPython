from sqlite3 import IntegrityError
from flask import Blueprint, redirect, render_template, request, flash, jsonify
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

@views.route('/create-ballot', methods=['GET', 'POST'])
@login_required
def create_ballot():

    students = models.Student.query.all()

    if request.method == 'POST':

        positions = [
            'president', 'vice_president', 'executive_board_sec', 'vp_finance',
            'vp_academic_affairs', 'vp_internal_external_affairs', 'vp_public_relations',
            'vp_research_dev', 'first_yr_rep', 'second_yr_rep', 'third_yr_rep', 'fourth_yr_rep'
        ]

        try:
            for position in positions:
                student_ids = [request.form.get(f'{position}_id{i}') for i in range(1, 5)]

                for student_id in student_ids:
                    student = models.Student.query.get(student_id)

                    if not student:
                        flash(f"Student with ID {student_id} not found.", category='error')
                        break 
                    
                    with db.session.no_autoflush:
                    # Check if a candidate with the same student ID and position already exists
                        existing_candidate = models.Candidate.query.filter_by(studentId=student.studentId, position=position).first()

                    if not existing_candidate:
                        candidate = models.Candidate(studentId=student.studentId, position=position, voteCount=0)
                        db.session.add(candidate)
                    else:
                        return jsonify({'success': False, 'message': f"There's a student ID in the same position that already exists for {position}."})

            db.session.commit()
            flash('Ballot created successfully!', category="success")
            return redirect('/create-ballot')

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error creating ballot. Please check for duplicate candidates.'})

    return render_template('create-ballot.html', students=students)

@views.route('/get_student_info/<student_id>', methods=['GET'])
def get_student_info(student_id):
    
    student = models.Student.query.filter_by(studentId=student_id).first()

    if student:
        return jsonify({'success': True, 'name': f'{student.firstName} {student.lastName}', 'course': student.course})
    else:
        return jsonify({'success': False})
    
@views.route('/check_duplicate/<student_id>/<position>/<int:index>', methods=['GET'])
@login_required
def check_duplicate(student_id, position, index):
    if not student_id:
        return jsonify({'isDuplicate': False, 'isExistInOtherPosition': False, 'index': index, 'error': 'Student ID is missing'})

    existing_candidate_same_position = models.Candidate.query.filter_by(studentId=student_id, position=position).first()

    existing_candidate_other_position = models.Candidate.query.filter_by(studentId=student_id).filter(models.Candidate.position != position).first()

    if existing_candidate_same_position:
        return jsonify({'isDuplicate': True, 'isExistInOtherPosition': False, 'index': index, 'error': f'Duplicate candidate for {position} with student ID {student_id}'})
    elif existing_candidate_other_position:
        return jsonify({'isDuplicate': True, 'isExistInOtherPosition': True, 'index': index, 'error': f'Student ID {student_id} already exists in another position'})
    else:
        return jsonify({'isDuplicate': False, 'isExistInOtherPosition': False, 'index': index})

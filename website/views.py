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
            
            ballot_name = request.form.get('ballot_name')
            ballot_status = models.BallotStatus(isOpen=True)
            db.session.add(ballot_status)
            db.session.commit()


            ballot = models.Ballot(user_id=current_user.userId, ballot_status=ballot_status, ballot_name=ballot_name)
            db.session.add(ballot)
            db.session.commit()

            for position in positions:
                student_ids = [request.form.get(f'{position}_id{i}') for i in range(1, 4)]

                for student_id in student_ids:
                    student = models.Student.query.get(student_id)

                    if not student:
                        flash(f"Student with ID {student_id} not found.", category='error')
                        break

                    # Check if a candidate with the same student ID and position already exists
                    existing_candidate = models.Candidate.query.filter_by(studentId=student.studentId, position=position).first()

                    if not existing_candidate:
                        candidate = models.Candidate(studentId=student.studentId, position=position, voteCount=0, ballot_id=ballot.id)
                        db.session.add(candidate)
                    else:
                        flash(f"There's a student ID in the same position that already exists for {position}.", 'error')
                        db.session.rollback()
                        return redirect('/create-ballot')

            db.session.commit()
            flash('Ballot created successfully!', category="success")
            return redirect('/create-ballot')

        except IntegrityError as e:
            db.session.rollback()
            flash(f'Error creating ballot: {str(e)}', category='error')

    return render_template('create-ballot.html', students=students)

@views.route('/get_student_info/<student_id>', methods=['GET'])
def get_student_info(student_id):
    student = models.Student.query.filter_by(studentId=student_id).first()

    if student:
        return jsonify({
            'success': True,
            'data': {
                'name': {'first': student.firstName, 'last': student.lastName},
                'course': student.course
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Student not found'
        })
      
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

@views.route('/get-ballot-status', methods=['GET'])
@login_required
def get_ballot_status():
    user_ballot = models.Ballot.query.filter_by(user_id=current_user.userId).first()

    if user_ballot:
        ballot_status = user_ballot.ballot_status

        if ballot_status:
            return jsonify({'success': True, 'isOpen': ballot_status.isOpen})
        else:
            return jsonify({'success': False, 'message': 'No ballot status found for this user.'})
    else:
        return jsonify({'success': False, 'message': 'No ballot found for this user.'})
    
@views.route('/ballots')
@login_required
def list_ballots():
    ballots = models.Ballot.query.all()
    return render_template('ballot-list.html', ballots=ballots)

@views.route('/toggle-ballot-status/<int:ballot_id>')
@login_required
def toggle_ballot_status(ballot_id):
    ballot = models.Ballot.query.get(ballot_id)

    if ballot:
        ballot_status = ballot.ballot_status

        if ballot_status:
            ballot_status.isOpen = not ballot_status.isOpen

            try:
                db.session.commit()
                flash('Ballot status updated successfully.', category='success')
                return redirect('/ballots')
            except Exception as e:
                db.session.rollback() 
                flash('Error committing changes to the database.', category='error')
        else:
            flash('Ballot status not found for this ballot.', category='error')

    flash('Ballot not found.', category='error')
    return redirect('/ballots')

@views.route('/delete-ballot/<int:ballot_id>')
@login_required
def delete_ballot(ballot_id):

    ballot = models.Ballot.query.get(ballot_id)

    if ballot:
        try:
            models.Candidate.query.filter_by(ballot_id=ballot.id).delete()

            models.BallotStatus.query.filter_by(id=ballot.ballot_status_id).delete()

            db.session.delete(ballot)
            db.session.commit()

            flash('Ballot deleted successfully!', category='success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting ballot: {str(e)}', category='error')

    return redirect('/ballots')

@views.route('/add-candidate/<int:ballot_id>', methods=['POST'])
@login_required
def add_candidate(ballot_id):
    ballot = models.Ballot.query.get(ballot_id)
    positions = [
        'president', 'vice_president', 'executive_board_sec', 'vp_finance',
        'vp_academic_affairs', 'vp_internal_external_affairs', 'vp_public_relations',
        'vp_research_dev', 'first_yr_rep', 'second_yr_rep', 'third_yr_rep', 'fourth_yr_rep'
    ]

    if request.method == 'POST':
        position = request.form['position']
        student_id = request.form['studentId']

        existing_candidate = models.Candidate.query.filter_by(position=position, studentId=student_id).first()

        if existing_candidate:
            flash(f"Student ID {student_id} already exists for a candidate in the same position.", category='error')
        else:
            try:
                new_candidate = models.Candidate(position=position, studentId=student_id, voteCount=0, ballot_id=ballot.id)
                db.session.add(new_candidate)
                db.session.commit()
                flash('Candidate added successfully!', category='success')
            except IntegrityError as e:
                db.session.rollback()
                flash(f'Error adding candidate: {str(e)}', category='error')

    candidates = models.Candidate.query.filter_by(ballot_id=ballot_id).all()

    set_student_info_for_candidates(candidates)

    return render_template('edit-ballot.html', ballot=ballot, candidates=candidates, positions=positions)

@views.route('/delete-candidate/<int:ballot_id>/<int:candidate_id>')
@login_required
def delete_candidate(ballot_id, candidate_id):
    candidate = models.Candidate.query.get(candidate_id)

    if candidate:
        try:
            db.session.delete(candidate)
            db.session.commit()

            flash('Candidate deleted successfully!', category='success')
        except IntegrityError as e:
            db.session.rollback()
            flash(f'Error deleting candidate: {str(e)}', category='error')

    candidates = models.Candidate.query.filter_by(ballot_id=ballot_id).all()

    set_student_info_for_candidates(candidates)

    return redirect(f'/edit-ballot/{ballot_id}')

@views.route('/edit-ballot/<int:ballot_id>', methods=['GET'])
@login_required
def edit_ballot(ballot_id):
    ballot = models.Ballot.query.get(ballot_id)
    candidates = models.Candidate.query.filter_by(ballot_id=ballot_id).all()

    set_student_info_for_candidates(candidates)

    return render_template('edit-ballot.html', ballot=ballot, candidates=candidates)

@views.route('/check_existing_candidate/<student_id>', methods=['GET'])
@login_required
def check_existing_candidate(student_id):
    try:
        if not student_id:
            return jsonify({'exists': False, 'error': 'Student ID is missing'})

        existing_candidate = models.Candidate.query.filter_by(studentId=student_id).first()

        return jsonify({'exists': existing_candidate is not None})
    except Exception as e:
        return jsonify({'exists': False, 'error': str(e)})

def set_student_info_for_candidates(candidates):
    student_ids = [candidate.studentId for candidate in candidates]

    students_info = {student.studentId: {'name': f"{student.firstName} {student.lastName}", 'course': student.course}
                     for student in models.Student.query.filter(models.Student.studentId.in_(student_ids)).all()}
    
    for candidate in candidates:
        student_id = candidate.studentId
        student_info = students_info.get(student_id)

        if student_info and isinstance(student_info, dict):
            candidate.student_name = student_info['name']
            candidate.student_course = student_info['course']
        else:
            candidate.student_name = ""
            candidate.student_course = ""     
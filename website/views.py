from sqlite3 import IntegrityError
from flask import Blueprint, redirect, url_for, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db, models, rules, socketio
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

# ROUTE FOR HOME/TIMELINE
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        userPostsCount = rules.getUserPostsCount()

        if userPostsCount >= 3:
            flash("You are only allowed for three (3) posts. Delete one of your posts, then try again.", "error")
        else:
            text = request.form.get('text')
            file = request.files['post-image']
            isFile = bool(file.filename.strip())
            isContinue = True

            imageDir = None
            imageSrc = None
            imageId = 0
            if db.session.query(models.Post.query.exists()).scalar():
                imageId = db.session.query(db.func.max(models.Post.id)).scalar() + 1

            if isFile:
                if not rules.allowed_file(file.filename):
                    flash("File is not an image file.", 'error')
                    # redirect(url_for('views.home'))
                    isContinue = False
                else:
                    fileName = secure_filename(file.filename)
                    imageSrc = f'../static/images/posts/{imageId}_{fileName}'
                    imageDir = f'website/static/images/posts/{imageId}_{fileName}'
                    file.save(imageDir)
            else:
                if len(text) < 1:
                    isContinue == False
                    flash("Post is empty.", 'error')
                    return redirect(url_for('views.home'))
                
            if isContinue:
                userId = current_user.userId
                userName = current_user.firstName + " " + current_user.lastName
                userRole = rules.getUserPostRole(current_user)
                
                post = models.Post(text=text, imageDir=imageDir, imageSrc=imageSrc, userName=userName, userId=userId, userRole=userRole)
                db.session.add(post)

                try:
                    db.session.commit()
                    return redirect(url_for('views.home'))
                except Exception as e:
                    db.session.rollback()
                    print(f"Error during data insertion: {e}")

    posts = rules.getSortedPostsByUserRole()

    if current_user.userType == "Admin":
        return render_template("timeline-admin.html", posts=posts, user=current_user)
    elif rules.isCandidate():
        return render_template("timeline-candidate.html", posts=posts, user=current_user)
    else:
        return render_template("timeline-student.html", posts=posts, user=current_user)

# ROUTE FOR DELETING A POST
@views.route('/timeline/delete-post/postId=<int:postId>', methods=['DELETE'])
def deletePost(postId):
    post = models.Post.query.get(postId)

    if post:
        if current_user.userType == "Admin" or post.userId == current_user.userId:
            if post.imageDir:
                os.remove(post.imageDir)

            db.session.delete(post)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'You are not allowed to delete this post.'})
    else:
        return jsonify({'success': False, 'message': 'An error occured. Please try again later.'})
    
# ROUTE FOR USER SETTINGS
@views.route('/settings')
@login_required
def settings():
    if current_user.userType == "Admin":
        return render_template('settings-admin.html', user=current_user)
    elif current_user.userType == "Student":
        return render_template('settings-student.html', user=current_user)

# ROUTE FOR VOTE
@views.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    current_ballot_status = models.BallotStatus.query.first()

    if current_ballot_status and current_ballot_status.ballotStatus == 'CLOSED':
        flash("Voting is closed.", "error")
        return redirect(url_for('views.home'))


    if rules.hasVoted() == True:
        flash("You have voted already. You can only vote once.", "error")
        return redirect(request.referrer)
    else:
        if request.method == 'POST':
            formData = request.form.to_dict()
            voter = current_user.userId

            vote = models.Vote(**formData, voter=voter)
            
            db.session.add(vote)

            try:
                db.session.commit()
                flash('Your vote is counted. Thank you.', category="success")
                socketio.emit('vote', rules.getVoteResults(), room=None)
                return redirect(url_for('views.home'))
            except Exception as e:
                db.session.rollback()
                print(f"Error during data insertion: {e}")
        
        return render_template('vote.html', candidates = rules.getCandidates(), current_ballot_status=current_ballot_status)

# ROUTE FOR VOTE LIVE RESULTS
@views.route('/live-results')
@login_required
def liveResults():
    return render_template("live-results.html", voteResults = rules.getVoteResults(), user=current_user)

@views.route('/ballot', methods=['GET', 'POST'])
@login_required
def ballot():

    candidates = {
        "president": models.Candidate.query.filter_by(position="president").all(),
        "executive_vp": models.Candidate.query.filter_by(position="executive_vp").all(),
        "executive_board_sec": models.Candidate.query.filter_by(position="executive_board_sec").all(),
        "vp_finance": models.Candidate.query.filter_by(position="vp_finance").all(),
        "vp_academic_affairs": models.Candidate.query.filter_by(position="vp_academic_affairs").all(),
        "vp_internal_affairs": models.Candidate.query.filter_by(position="vp_internal_affairs").all(),
        "vp_external_affairs": models.Candidate.query.filter_by(position="vp_external_affairs").all(),
        "vp_public_relations": models.Candidate.query.filter_by(position="vp_public_relations").all(),
        "vp_research_dev": models.Candidate.query.filter_by(position="vp_research_dev").all(),
        "first_yr_rep": models.Candidate.query.filter_by(position="first_yr_rep").all(),
        "second_yr_rep": models.Candidate.query.filter_by(position="second_yr_rep").all(),
        "third_yr_rep": models.Candidate.query.filter_by(position="third_yr_rep").all(),
        "fourth_yr_rep": models.Candidate.query.filter_by(position="fourth_yr_rep").all()
    }

    current_ballot_status = models.BallotStatus.query.first()

    if request.method == 'POST':
        update_ballot_status()

    return render_template('ballot.html', candidates=candidates, current_ballot_status=current_ballot_status)

@views.route('/ballot/delete-candidate/<string:studentId>', methods=['DELETE'])
def deleteCandidate(studentId):
    candidate = models.Candidate.query.filter_by(studentId=studentId).first()

    if candidate:
        db.session.delete(candidate)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Candidate successfully deleted.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Candidate not found.'}), 404

@views.route('/ballot/add-candidate', methods=['POST'])
def addCandidate():

    if request.method == 'POST':
        user_id_input = request.form.get('user-id-input')

        # Check if a candidate with the given user ID already exists
        existing_candidate = models.Candidate.query.filter_by(studentId=user_id_input).first()

        if existing_candidate:
            flash('Candidate already exists.', category='error')
            return redirect('/ballot')

        else:
            user = models.User.query.get(user_id_input)

            if user:
                first_name = user.firstName
                last_name = user.lastName

                position = request.form.get('position')

                new_candidate = models.Candidate(studentId=user.userId, name=f"{first_name} {last_name}", position=position)

                db.session.add(new_candidate)

                try:
                    db.session.commit()
                    flash('Candidate added successfully.', category='success')
                except IntegrityError:
                    db.session.rollback()
                    flash('Candidate already exists.', category='error')
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error adding candidate: {e}", category='error')
                    
            return redirect('/ballot')

    return render_template('ballot.html')
    
@views.route('/ballot/status', methods=['POST'])
def update_ballot_status():
    ballot_status = models.BallotStatus.query.first()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'open' and ballot_status.ballotStatus == 'NEW':
            ballot_status.ballotStatus = 'OPEN'
            db.session.commit()
            flash('Ballot is now open!', 'success')
            return jsonify({'success': True})
        
        elif action == 'close' and ballot_status.ballotStatus == 'OPEN':
            ballot_status.ballotStatus = 'CLOSED'
            db.session.commit()
            flash('Ballot is now closed!', 'success')
            return jsonify({'success': True})
        else:
            flash('Invalid action or the ballot is already in the desired status.', 'error')

    return jsonify({'success': False})

@views.route('/clear-ballot', methods=['GET', 'POST'])
def clearballot():
    ballot_status = models.BallotStatus.query.first()

    if ballot_status.ballotStatus == 'CLOSED':
        try:
            # Clear all posts, votes, and candidates
            models.Post.query.delete()
            models.Vote.query.delete()
            models.Candidate.query.delete()

            # Reset BallotStatus to a new state
            ballot_status.ballotStatus = 'NEW'
            db.session.commit()

            flash('Ballot cleared successfully!', category='success')
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            flash(f'Error clearing ballot: {str(e)}', category='error')
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    else:
        flash('Cannot clear the ballot. Please close the ballot first.', category='error')
        return jsonify({'success': False, 'message': 'Ballot is not closed.'}), 400
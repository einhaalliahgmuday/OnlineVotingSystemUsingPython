from flask import Blueprint, render_template, request, flash, jsonify
# from flask_login import login_required, current_user
# from .models import Note
# from . import db
import json

views = Blueprint('views', __name__)

@views.route('/select-user-type')
def selectUserType():
    return render_template('select-user-type.html')

@views.route('/')
# @login_required
def home():
    

    return render_template("home.html") #user=current_user

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#             return jsonify({})

    
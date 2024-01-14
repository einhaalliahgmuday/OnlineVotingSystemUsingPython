from . import db 
from flask_login import UserMixin
# from sqlalchemy.sql import func

class Student(db.Model, UserMixin):
    studentId = db.Column(db.String(15), primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Admin(db.Model, UserMixin):
    adminId = db.Column(db.String(15), primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)
    studentId = db.Column(db.String(15), db.ForeignKey('student.studentId'), nullable=False, unique=True)
    voteCount = db.Column(db.Integer)
    posts = db.relationship('Post')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    image = db.Column(db.LargeBinary)
    studentId = db.Column(db.String(15), db.ForeignKey('student.studentId'), nullable=False)
    

class Vote(db.Model):
    voter = db.Column(db.String(15), db.ForeignKey('student.studentId'), primary_key=True, nullable=False)
    president = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    vice_president = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    executive_board_sec = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    vp_finance = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    vp_academic_affairs = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    vp_internal_external_affairs = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    vp_public_relations = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    vp_research_dev = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    first_yr_rep = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    second_yr_rep = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    third_yr_rep = db.Column(db.String(15), db.ForeignKey('student.studentId'))
    fourth_yr_rep = db.Column(db.String(15), db.ForeignKey('student.studentId'))
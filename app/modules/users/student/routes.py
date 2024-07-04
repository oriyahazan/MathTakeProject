from flask import Blueprint, render_template, request, redirect, url_for, session
import pymongo
from modules.users.models import User
from modules.users.student.models import Student


student_bp = Blueprint('student_bp', __name__)

client = pymongo.MongoClient("mongodb+srv://Osnat:123456!@cluster1.7pvmkvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client.get_database("total_records")
questionnaire_collection = db.questionnaire

@student_bp.route("/indexStudent", methods=['GET'])
def displayStudentHome():
    return render_template('student/indexStudent.html')

@student_bp.route("/questionnaire", methods=['GET'])
def questionnaire():
    email = request.args.get('email')
    parent_email = request.args.get('parent_email')
    name = request.args.get('name')
    return render_template('student/questionnaire.html',name = name, email=email, parent_email=parent_email)


@student_bp.route("/submit_questionnaire", methods=['POST'])
def submit_questionnaire():
    form_data = request.form.to_dict()

    questionnaire_data = {
        "student_email": form_data.get('email'),
        "parent_email": form_data.get('parent_email'),
        "full_name": form_data.get('fullName'),
        "grade": form_data.get('grade'),
        "rating": form_data.get('rating'),
        "first_subject": form_data.get('firstSubject'),
        "second_subject": form_data.get('secondSubject'),
    }
    questionnaire_collection.insert_one(questionnaire_data)

    # Redirect to home page for Student
    return render_template('student/indexStudent.html')
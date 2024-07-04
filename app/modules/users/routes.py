from flask import Blueprint, render_template, request, redirect, url_for, session
import pymongo
from modules.users.student.models import Student
from modules.users.teacher.models import Teacher
from modules.users.parent.models import Parent



# Create a blueprint named 'users_bp'
users_bp_main = Blueprint('users_bp_main', __name__)

client = pymongo.MongoClient("mongodb+srv://Osnat:123456!@cluster1.7pvmkvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client.get_database("total_records")

@users_bp_main.route("/signup", methods=['GET'])
def signup_form():
    return render_template("signupPage.html")


@users_bp_main.route("/signup", methods=['POST'])
def signup():
    # data = request.form
    data = request.form.to_dict() 
    email = data.get('email')

    # Check if email already exists 
    if db.parents.find_one({"email": email}) or db.teacher.find_one({"email": email}) or  db.students.find_one({"email": email}):
        return render_template("signup.html", error="Email already exists. Please use a different email.")

    # Check if user is a student and validate parent's email
    if data.get('role') == 'Student':
        parent_email = data.get('parent_email')
        parent = db.parents.find_one({"email": parent_email, "role": "Parent"})
        if not parent:
            return render_template("signup.html", error="Parent email not found. Please provide a valid parent email.")

        # Find and update the parent's document
        db.parents.update_one(
            {"email": parent_email},
            {"$addToSet": {"students": data['email']}}
        )

        # Add parent's email to student's data
        data["parent_email"] = parent_email
    
    if data.get('role') == 'Student':
        user = Student().signup(data)
        db.students.insert_one(user)
        return redirect(url_for('student_bp.questionnaire', name=data['name'], email=data['email'], parent_email=data['parent_email']))
    
    elif data.get('role') == 'Parent':
        user = Parent().signup(data)
        db.parents.insert_one(user)

    else: 
        user = Teacher().signup(data)
        db.teachers.insert_one(user)

    return redirect(url_for('home'))

@users_bp_main.route("/login", methods=['GET'])
def login_form():
    return render_template("login.html")


@users_bp_main.route("/login", methods=['POST'])
def login():
    data = request.form
    email = data.get('email') 
    password = data.get('password')
    session['email'] = email
    print(email)

    # if db.parents.find_one({"email": email, "password": password}): 
    #     return redirect(url_for('indexParent')) 

    if db.parents.find_one({"email": email, "password": password}): 
        return render_template("indexParent.html")

    elif db.teacher.find_one({"email": email, "password": password}): 
        return render_template("indexTeacher.html")
    
    elif db.student.find_one({"email": email, "password": password}): 
        return render_template("indexStudent.html")

    else:
        # Login failed
        return render_template("indexParent.html", error="Invalid username or password.")

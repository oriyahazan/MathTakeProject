from flask import Flask,render_template, request, url_for, redirect,session
import pymongo
from modules.users.routes import users_bp_main 
from modules.users.student.routes import student_bp 

import secrets

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://Osnat:123456!@cluster1.7pvmkvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client.get_database("total_records")
app.secret_key = secrets.token_hex(16)


# app.register_blueprint(users_bp)
app.register_blueprint(users_bp_main, url_prefix='/users')
app.register_blueprint(student_bp, url_prefix='/student')



# @app.route("/", methods=['GET'])
# def home():
#     fullName = session.get('fullName')
#     return render_template("index.html", fullName=fullName)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

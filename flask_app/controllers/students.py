from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import student, classs
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/createstudent', methods=['POST'])
def add_student():
    check=student.Student.validate_student(request.form)
    print(check)
    if check:
        student.Student.create_student(request.form)
        logged_in_student=student.Student.login_student(request.form)
        print(session['id'])
        return render_template ("dashboard.html")
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    logged_in_student=student.Student.login_student(request.form)
    if logged_in_student:
        return redirect("/dashboard")
    return redirect ('/')


@app.route ('/dashboard')
def dashboardpage():
    Student=student.Student.get_all_logged_in_students_classes()
    if Student:
        all_my_classes=Student.classes
        return render_template('dashboard.html',all_classes=classs.Class.get_all_classes(),all_my_classes=all_my_classes,hello='hello')
    return render_template('dashboard.html',all_classes=classs.Class.get_all_classes())

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect('/')

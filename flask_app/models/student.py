from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import classs
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# model the class after the friend table from our database
class Student:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.email = data['email']
        self.password = data ['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.classes = []
    
    @staticmethod
    def validate_student( form ):
        is_valid = True
        query = """SELECT * FROM students WHERE email =  %(email)s"""
        results = connectToMySQL('students_classes').query_db(query, form)
        if len(results) >= 1:
            flash("email address already in use!")
            is_valid = False
        elif not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(form['first_name']) < 3:
            flash("First Name must be 3 Characters!")
            is_valid = False
        if len(form['last_name']) <  3:
            flash("Last Name must be 3 Characters!")
            is_valid = False
        if int(form['age']) < 18:
            flash("Students must be 18 in order to enroll!")
            is_valid = False
        if form['passwordcheck'] != form['password']:
            flash('passwords do not match!')
            is_valid = False
        return is_valid

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL('recipes_schema').query_db(query)
    #     # Create an empty list to append our instances of friends
    #     users = []
    #     # Iterate over the db results and create instances of friends with cls.
    #     for user in results:
    #         users.append( cls(user)) 
    #     return users

    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM users where id = %(id)s;"
    #     results = connectToMySQL('recipes_schema').query_db(query,data)
    #     return cls(results[0])
    
    @classmethod
    def create_student(cls, form):
        data = {
                'first_name' : form['first_name'],
                'last_name' : form['last_name'],
                'age' : form['age'],
                'email' : form['email'],
                'password' : bcrypt.generate_password_hash(form['password'])
            }
        query = """INSERT INTO students (first_name, last_name, age, email, password) 
        VALUES (%(first_name)s,%(last_name)s, %(age)s,%(email)s, %(password)s);"""
        return connectToMySQL('students_classes').query_db( query, data )
    
    @classmethod
    def login_student(cls, form):
        query = """SELECT * FROM students WHERE email =  %(email)s"""
        results = connectToMySQL('students_classes').query_db(query, form)
        print(results)
        if len(results)<1:
            flash('Username or Password Incorrect')
            return False
        elif not bcrypt.check_password_hash(results[0]['password'], form['password'] ):
            flash('Username or Password Incorrect')
            return False
        logged_in_student=cls(results[0])
        session['id'] =logged_in_student.id
        session['first_name']=logged_in_student.first_name
        return True

    @classmethod
    def get_all_logged_in_students_classes(cls):
        query = """SELECT * FROM students 
        JOIN enrollments ON enrollments.student_id = students.id 
        JOIN classes ON enrollments.class_id = classes.id 
        WHERE students.id = '%(id)s' ;"""
        data = {
            'id': session['id']
        }
        results = connectToMySQL('students_classes').query_db(query,data)
        if results:
            student = cls(results[0])
            for row in results:
                one_class= {
                    "id": row['classes.id'], 
                    "name": row['name'],
                    "content": row['content'],
                    "created_at": row['classes.created_at'],
                    "updated_at": row['classes.updated_at']
                }
                student.classes.append(classs.Class(one_class))
            return student
        return False
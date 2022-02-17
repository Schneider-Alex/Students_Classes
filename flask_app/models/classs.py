from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import student
bcrypt = Bcrypt(app)

class Class:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.enrolled_students=[]

    @staticmethod
    def validate_class(form):
        is_valid = True
        query = """SELECT * FROM classes WHERE name =  %(name)s"""
        data= {
            'name':form['name']
        }
        results = connectToMySQL('students_classes').query_db(query,data)
        if results:
            flash("This class already exists!")
            is_valid = False
        if len(form['name']) < 3:
            flash("Recipe Name must be 3 Characters!")
            is_valid = False
        if len(form['content']) <  3:
            flash("Content must be 3 Characters! What is this class about?")
            is_valid = False
        return is_valid
        
    @classmethod
    def get_all_classes(cls):
        query = "SELECT * FROM classes;"
        results = connectToMySQL('students_classes').query_db(query)
        classes = []
        if not len(results)<1:
            for class_ in results:
                classes.append( cls(class_)) 
        return classes
        
    @classmethod
    def get_one_class(cls, classid):
        data={
            'id': classid
        }
        query = "SELECT * FROM classes where id = %(id)s;"
        results = connectToMySQL('students_classes').query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_students_in_class(cls,classid):
        query = """SELECT * FROM classes 
        JOIN enrollments ON enrollments.class_id = classes.id 
        JOIN students ON enrollments.student_id = students.id 
        WHERE classes.id = '%(id)s' ;"""
        data = {
            'id': classid
        }
        results = connectToMySQL('students_classes').query_db(query,data)
        if results:
            classs = cls(results[0])
            for row in results:
                one_student= {
                    "id": row['students.id'], 
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "age": row['age'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['students.created_at'],
                    "updated_at": row['students.updated_at']
                }
                classs.enrolled_students.append(student.Student(one_student))
            return classs
        return False

    @classmethod
    def delete_class(cls, data):
        query="""DELETE FROM classes WHERE classes.id = %(id)s"""
        return connectToMySQL('students_classes').query_db( query, data )

    @classmethod
    def create_class(cls,form):
        data={
            'name': form['name'],
            'content':form['content'],
        }
        query = """INSERT INTO classes (name, content) 
        VALUES (%(name)s, %(content)s);"""
        return connectToMySQL('students_classes').query_db( query, data )
    
    @classmethod
    def update_class(cls,form):
        data ={
            'id' : form['id'],
            'name':form['name'],
            'content' : form['content']
        }
        query = """UPDATE classes
        SET name = %(name)s, content = %(content)s, updated_at = NOW()
        WHERE id=%(id)s;"""
        return connectToMySQL('students_classes').query_db( query, data )

    @classmethod
    def get_this_enrollment(cls,data):
        query = "SELECT * FROM enrollments WHERE student_id = %(student_id)s AND class_id = %(class_id)s;"
        return connectToMySQL('students_classes').query_db(query,data)

    @classmethod
    def enroll_logged_in_student_in_class(cls,classid):
        data={
                'student_id': session['id'],
                'class_id': classid,
            }
        if Class.get_this_enrollment(data):
            flash('you are already enrolled in that class!')
            return False
        query = """INSERT INTO enrollments (student_id, class_id) 
        VALUES (%(student_id)s, %(class_id)s);"""
        flash('You have succesfully enrolled!')
        return connectToMySQL('students_classes').query_db( query, data )




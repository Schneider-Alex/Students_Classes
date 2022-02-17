from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import student, classs
from flask import flash


@app.route('/createclass',methods=['GET'])
def trasnfer_to_create_class_page():
    if session:
        return render_template('newclasspage.html')
    else:
        return redirect('/')


@app.route('/classes/new',methods=['POST'])
def new_class():
    check=classs.Class.validate_class(request.form)
    if check:
        classs.Class.create_class(request.form)
        return redirect('/dashboard')
    return redirect('/createclass')

@app.route('/class/edit/<int:classid>')
def edit_class_page(classid):
    return render_template('edit_class_page.html',this_class=classs.Class.get_one_class(classid))

@app.route('/editclass',methods=['POST'])
def edit_class():
    classs.Class.update_class(request.form)
    classid=request.form['id']
    return redirect (f'/class/{classid}')

@app.route('/class/<int:classid>')
def display_class_detail(classid):
        Class=classs.Class.get_all_students_in_class(classid)
        if Class:
            this_classes_students=Class.enrolled_students
            return render_template('class_page.html', this_class=classs.Class.get_one_class(classid),this_classes_students=this_classes_students)
        return render_template('class_page.html', this_class=classs.Class.get_one_class(classid))

@app.route('/class/enroll/<int:classid>')
def enrollment(classid):
    if session:
        check=classs.Class.enroll_logged_in_student_in_class(classid)
        return redirect('/dashboard')
    flash('you must be logged in to view this page!')
    return redirect('/')


# @app.route('/recipe/delete/<recipeid>')
# def deleterecipe(recipeid):
#     data = {
#         'id' : recipeid
#     }
#     recipe.Recipe.delete_recipe(data)
#     return redirect ('/dashboard')

# @app.route('/recipe/<int:recipeid>')
# def show_recipe(recipeid):
#     data = {
#         'id':  recipeid
#     }
#     this_recipe=recipe.Recipe.get_one_recipe(data)
#     log_in_data={
#                 'id' : session['id']
#             }
#     if this_recipe:
#         creator_data={
#             'id' : this_recipe.users_id
#         }
#         return render_template('recipe_page.html',this_recipe=this_recipe, creator=user.User.get_one(creator_data),user=user.User.get_one(log_in_data))
#     else:
#         return redirect('/dashboard')

# @app.route('/recipe/edit/<int:recipeid>')
# def edit_recipe_page(recipeid):
#     data = {
#         'id':  recipeid
#     }
#     this_recipe=recipe.Recipe.get_one_recipe(data)
#     return render_template("edit_recipe_page.html", this_recipe=this_recipe)

# @app.route('/editrecipe', methods=["POST"])
# def edit_recipe():
#     data= {
#         'id' : request.form['id'],
#         'name' : request.form['name'],
#         'instructions' : request.form['instructions'],
#         'description' : request.form['description'],
#         'under_thirty' : request.form['under_thirty'],
#     }
#     recipe.Recipe.update_recipe(data)
#     return redirect ('/dashboard')



from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import datetime
import os
from app import app
from app.forms import LoginForm, ChangePasswordForm, TodoForm
import json
from app import db
from app import Todo

JSON_FILE = os.path.join(app.static_folder, 'data/login.json')

skills = ["java", "c++", "mysql", "python"]

@app.route('/')
@app.route('/about')
def about_page():
    return render_template('about.html', os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())

@app.route('/skills')
@app.route('/skills/<int:id>')
def skills_page(id=None):
    if id is not None and id < len(skills):
        return render_template('skill.html', skill=skills[id])
    else:
        return render_template('skills.html', skills=skills)

@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if"username" in session:
        return redirect(url_for("admin_page"))   
    
    form = LoginForm()

    if  form.validate_on_submit(): 
        username = form.name.data
        password = form.password.data
        remember = form.remember.data

        with open(JSON_FILE) as f:
            users = json.load(f).get("users")
            if any(user.get("name") == username and user.get("password") == password for user in users): 
                if remember:
                    session["username"] = username
                    flash("Logged in successfully!!", category="success")
                    return redirect(url_for("admin_page"))
                
                flash("Logged in successfully to about!!", category="success")
                return redirect(url_for("about_page"))

            flash("Wrong data! Try again!", category="danger")
            return redirect(url_for("login"))
    
    return render_template('login.html', form=form)

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    flash("Logged out successfully!!", category="success")
    return redirect(url_for("login"))

@app.route('/admin')
def admin_page():
    form = ChangePasswordForm()

    if "username" not in session:
        flash("You need to login first!", category="danger")
        return redirect(url_for("login"))

    return render_template('admin.html', username=session.get("username"), cookies=request.cookies, form=form)


@app.route('/cookies', methods=["POST"])
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    exp_date = request.form.get("date")

    if key and value and exp_date:
        response = make_response(redirect(url_for("admin_page")))
        response.set_cookie(key, value, expires=datetime.strptime(exp_date, "%Y-%m-%dT%H:%M"))
        flash(f"Success! {key} : {value} was added.", category="success")
        return response

    flash("Failed!", category="danger")
    return redirect(url_for("admin_page"))

@app.route('/cookies/delete', methods=["POST"])
@app.route('/cookies/delete/<key>', methods=["POST"])
def delete_cookie(key = None):
    response = make_response(redirect(url_for("admin_page")))

    if key:
        response.delete_cookie(key)
        flash(f"Success! Cookie: {key} was deleted.", category="success")
    else:
        for key in request.cookies.keys():
            response.delete_cookie(key)
    
    return response

@app.route('/change-password', methods=["POST"])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        old = form.old_password.data
        new = form.new_password.data
        username = session.get("username")

        file =  open(JSON_FILE, "r")
        data = json.load(file)
        file.close()    
        users = data.get("users")

        index = next((i for i, user in enumerate(users) if user.get("name") == username), -1)

        if index >= 0 and users[index].get("password") == old:
            users[index]["password"] = new
            file = open(JSON_FILE, "w+")
            file.write(json.dumps(data))
            file.close() 
            flash("Password changed!", category="success")
        else:
            flash("Failed!", category="danger")
    else:
        flash("Validation error!", category="danger")
    
    return redirect(url_for("admin_page"))

@app.route('/todos')
def todos():
    todo_list = db.session.query(Todo).all()
    return render_template("todo.html", todo_list=todo_list, form=TodoForm())
 
@app.route("/todos/add", methods=["POST"])
def add_todo():
    form=TodoForm()
    new_todo = Todo(title=form.title.data, due_date=form.due_date.data, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todos"))
 
@app.route("/todos/update/<int:id>")
def update_todo(id):
    todo = db.get_or_404(Todo, id)
    todo.complete = not todo.complete   
    db.session.commit()
    return redirect(url_for("todos"))
 
@app.route("/todos/delete/<int:id>")
def delete_todo(id):
    todo = db.get_or_404(Todo, id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todos"))

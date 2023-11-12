from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import datetime
import os
from app import app, db
from app.forms import LoginForm, ChangePasswordForm, TodoForm, FeedbackForm,RegistrationForm
from app.models import Todo, Feedback, User

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    session.pop('email', None)
    form = RegistrationForm()
    
    if form.validate_on_submit():
        new_user = User(name=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {form.username.data}!", "success")
        except:
            db.session.rollback()
            flash("Something went wrong!", category="danger")
        return redirect(url_for("login"))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if"email" in session:
        return redirect(url_for("admin_page"))   
    
    form = LoginForm()

    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.verify_password(form.password.data): 
            if form.remember.data:
                session["email"] = form.email.data
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

@app.route('/users')
def users():
    return render_template('users.html', users=User.query.all())

@app.route('/admin')
def admin_page():
    form = ChangePasswordForm()

    if "email" not in session:
        flash("You need to login first!", category="danger")
        return redirect(url_for("login"))

    return render_template('admin.html', username=session.get("email"), cookies=request.cookies, form=form)


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
        user = User.query.filter_by(email=session.get("email")).first()

        if user and user.verify_password(form.old_password.data):
            try:
                user.password = form.new_password.data
                db.session.commit()
                flash("Password changed!", category="success")
            except:
                db.session.rollback()
                flash("Failed!", category="danger")
        else:
            flash("Wrong data! Try again!", category="danger")
    else:
        flash("Validation error!", category="danger")
    
    return redirect(url_for("admin_page"))

@app.route('/todos')
def todos():
    todo_list = Todo.query.all()
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
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete   
    db.session.commit()
    return redirect(url_for("todos"))
 
@app.route("/todos/delete/<int:id>")
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todos"))

@app.route('/feedbacks', methods=["GET", "POST"])
def feedbacks():
    form=FeedbackForm()

    if form.validate_on_submit():
        new_feedback = Feedback(
            topic= form.topic.data,
            text=form.text.data,
            mark=form.mark.data,
            user_email=form.email.data,  
            date=datetime.now())
        
        try:
            db.session.add(new_feedback)
            db.session.commit()
            flash("Feedback added!", category="success")
        except:
            db.session.rollback()
            flash("Something went wrong!", category="danger")
        return redirect(url_for("feedbacks"))

    feedbacks = Feedback.query.all()
    return render_template("feedbacks.html", feedbacks=feedbacks, form=form)
 
@app.route("/feedbacks/delete/<int:id>")
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", category="success")
    except:
        db.session.rollback()
        flash("Something went wrong!", category="danger")
    
    return redirect(url_for("feedbacks"))

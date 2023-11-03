from flask import render_template, request, redirect, url_for, make_response, session
from datetime import datetime
import os
from app import app
import json

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
        return render_template('skill.html', skill=skills[id], os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())
    else:
        return render_template('skills.html', skills=skills, os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())

@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("name")
        password = request.form.get("password")

        with open(JSON_FILE) as f:
            users = json.load(f).get("users")
            if any(user["name"] == username and user["password"] == password for user in users): 
                session["username"] = username
                return redirect(url_for("info_page"))
            else:
                session["error_message"] = "Wrong data! Try again!"
                return redirect(url_for("login"))
    
    if session.get("username"):
        return redirect(url_for("info_page"))   

    return render_template('login.html', message=session.pop("error_message", None), os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/info')
def info_page():
    if not session.get("username"):
        return redirect(url_for("login"))

    return render_template('info.html', username=session.get("username"),message=session.pop("message", None),cookies=request.cookies, os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())


@app.route('/cookies', methods=["POST"])
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    exp_date = request.form.get("date")

    if key and value and exp_date:
        response = make_response(redirect(url_for("info_page")))
        response.set_cookie(key, value, expires=datetime.strptime(exp_date, "%Y-%m-%dT%H:%M"))
        session["message"] = {"successfully": True, "text": f"Success! {key} : {value} was added."}
        return response

    session["message"] = {"successfully": False, "text": "Failed!"}
    return redirect(url_for("info_page"))

@app.route('/cookies/delete', methods=["POST"])
@app.route('/cookies/delete/<key>', methods=["POST"])
def delete_cookie(key = None):
    response = make_response(redirect(url_for("info_page")))

    if key:
        response.delete_cookie(key)
        session["message"] = {"successfully": True, "text": f"Success! cookie: {key} was deleted."}
    else:
        for key in request.cookies.keys():
            response.delete_cookie(key)
    
    return response

@app.route('/change-password', methods=["POST"])
def change_password():
    old = request.form.get("old")
    new = request.form.get("new")
    username = session.get("username")

    file =  open(JSON_FILE, "r")
    data = json.load(file)
    file.close()    
    users = data.get("users")

    index = next((i for i, user in enumerate(users) if user["name"] == username), -1)

    if index >= 0 and users[index]["password"] == old:
        users[index]["password"] = new
        file = open(JSON_FILE, "w+")
        file.write(json.dumps(data))
        file.close() 
        session["message"] = {"successfully": True, "text": "Password changed!"}
    else:
        session["message"] = {"successfully": False, "text": "Failed!"}

    return redirect(url_for("info_page"))

from flask import render_template, request
from datetime import datetime
import os
from . import resume_bp

skills = ["java", "c++", "mysql", "python"]

@resume_bp.route('/')
@resume_bp.route('/about')
def about_page():
    return render_template('resume/about.html', os=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())

@resume_bp.route('/skills')
@resume_bp.route('/skills/<int:id>')
def skills_page(id=None):
    if id is not None and id < len(skills):
        return render_template('resume/skill.html', skill=skills[id])
    else:
        return render_template('resume/skills.html', skills=skills)

@resume_bp.route('/contacts')
def contacts_page():
    return render_template('resume/contacts.html')

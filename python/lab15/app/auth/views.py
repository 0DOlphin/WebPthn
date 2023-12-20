from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from ..extensions import db
from .forms import LoginForm, ChangePasswordForm, RegistrationForm, UpdateAccountForm
from .models import User
from ..util import save_thumbnail
from . import auth_bp


@auth_bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {new_user.username}!", "success")
            return redirect(url_for("auth.login"))
        except:
            db.session.rollback()
            flash("Something went wrong!", category="danger")
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.account'))
    
    form = LoginForm()

    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.verify_password(form.password.data): 
            login_user(user, remember=form.remember.data)
            flash("Logged in successfully!!", category="success")    
            return redirect(url_for('auth.account'))

        flash("Wrong data! Try again!", category="danger")
        return redirect(url_for("auth.login"))
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!!", category="success")
    return redirect(url_for("auth.login"))

@auth_bp.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('auth/account.html', password_form=ChangePasswordForm(), info_form=UpdateAccountForm())

@auth_bp.route('/change-password', methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            try:
                current_user.password = form.new_password.data
                db.session.commit()
                logout_user()
                flash("Password changed!", category="success")
                return redirect(url_for("auth.login"))
            except:
                db.session.rollback()
                flash("Failed!", category="danger")
        else:
            flash("Wrong data! Try again!", category="danger")
        return redirect(url_for("auth.account"))
    
    flash("Validation error!", category="danger")
    return render_template('auth/account.html', password_form=form, info_form=UpdateAccountForm())

@auth_bp.route('/update-user', methods=["POST"])
@login_required
def update_user():
    form = UpdateAccountForm(current_user=current_user)

    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_thumbnail(form.picture.data)
        try:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash("Info updated!", category="success")
        except:
            db.session.rollback()
            flash("Failed!", category="danger")
        return redirect(url_for("auth.account"))

    flash("Validation error!", category="danger")
    return render_template('auth/account.html', password_form=ChangePasswordForm(), info_form=form)

@auth_bp.route('/users')
@login_required
def users():
    return render_template('auth/users.html', users=User.query.all())
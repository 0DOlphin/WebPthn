from flask import render_template, redirect, url_for, flash
from datetime import datetime
from ..extensions  import db
from .forms import FeedbackForm
from .models import Feedback
from . import feedbacks_bp


@feedbacks_bp.route('/', methods=["GET", "POST"])
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
        return redirect(url_for("feedbacks.feedbacks"))

    feedbacks = Feedback.query.all()
    return render_template("feedbacks/feedbacks.html", feedbacks=feedbacks, form=form)
 
@feedbacks_bp.route("/delete/<int:id>")
def delete(id):
    feedback = Feedback.query.get_or_404(id)
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", category="success")
    except:
        db.session.rollback()
        flash("Something went wrong!", category="danger")
    
    return redirect(url_for("feedbacks.feedbacks"))

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    text = TextAreaField(label='Text', validators=[DataRequired("Text is required")])
    topic = StringField(label='Topic', validators=[DataRequired("Topic is required")])
    mark =  RadioField(choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],
                       validators=[DataRequired("Mark is required")])
    email = EmailField(label='User email', validators=[DataRequired("Email is required")])
    submit = SubmitField(label="Save")

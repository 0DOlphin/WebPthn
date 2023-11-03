from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, RadioField, EmailField
from wtforms.validators import DataRequired, Length, Email




class LoginForm(FlaskForm):
    name = StringField(label='User name', validators=[DataRequired("User name is required")])
    password = PasswordField(label='Password', validators=[
            DataRequired("Password is required"), 
            Length(min=4, max=10, message="Min length - 4, max - 10 symbols")
        ])
    remember = BooleanField(label="Remember me")
    submit = SubmitField(label="Sign in")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(label='Old password', validators=[
            DataRequired("Old password is required"), 
            Length(min=4, max=10, message="Min length - 4, max - 10 symbols")
        ])
    new_password = PasswordField(label='New password', validators=[
            DataRequired("New password is required"), 
            Length(min=4, max=10, message="Min length - 4, max - 10 symbols")
        ])
    submit = SubmitField(label="Save changes")

class TodoForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired("Title is required")])
    due_date = DateField(label='Due date')
    submit = SubmitField(label="Save")

class FeedbackForm(FlaskForm):
    text = TextAreaField(label='Text', validators=[DataRequired("Text is required")])
    topic = StringField(label='Topic', validators=[DataRequired("Topic is required")])
    mark =  RadioField(choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],
                       validators=[DataRequired("Mark is required")])
    email = EmailField(label='User email', validators=[DataRequired("Email is required")])
    submit = SubmitField(label="Save")


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Length, Regexp
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    badge = StringField("Badge", validators=[DataRequired()]) 
    company = StringField('Company', validators=[Length(max=150)]) # Added company field
    # Using PasswordField for PIN for masking
    pin = PasswordField("PIN", validators=[
        DataRequired(),
        Length(min=4, max=6, message='PIN must be between 4 and 6 digits long.'),
        Regexp(r'^[0-9]{4,6}$', message='PIN must consist of 4 to 6 digits only.')
    ])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

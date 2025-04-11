from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField,BooleanField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
    Optional,
    NumberRange,
)
from app.models import User

class RegistrationForm(FlaskForm):
    fname = StringField(
        "First Name:", validators=[DataRequired(), Length(min=2, max=25)]
    )
    lname = StringField("Last Name:", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(
        "Username:", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password:",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$",
                message="Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password:", validators=[DataRequired(), EqualTo("password")]
    )
    gender = SelectField(
        "Gender:",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other"), ("Prefer not to say", "Prefer not to say")],
        validators=[DataRequired()],
    )
    phone_number = StringField(
        "Phone Number:",
        validators=[
            Optional(),
            Regexp(r'^\+?[1-9]\d{7,14}$', message="Invalid phone number format. Must be 8 to 15 digits"),
        ],
        description="Optional phone number (8-15 digits). May include + and country code",
    )
    home_address = TextAreaField("Home Address:", validators=[Optional()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please choose a different one"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists! Please choose a different one")

class LoginForm(FlaskForm):
    email = StringField("Address E-mail :", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password :",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Request ')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
    
class UpdateProfileForm(FlaskForm):
    fname = StringField(
        "First Name:", validators=[DataRequired(), Length(min=2, max=25)]
    )
    lname = StringField("Last Name:", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(
        "Username:", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Address E-mail :", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio :")
    gender = SelectField(
        "Gender:",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other"), ("Prefer not to say", "Prefer not to say")],
        validators=[DataRequired()],
    )
    phone_number = StringField(
        "Phone Number:",
        validators=[
            Optional(),
            Regexp(r'^\+?[1-9]\d{7,14}$', message="Invalid phone number format. Must be 8 to 15 digits"),
        ],
        description="Optional phone number (8-15 digits). May include + and country code",
    )
    home_address = TextAreaField("Home address :")
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already exists! Please choose a different one"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email already exists! Please choose a different one"
                )


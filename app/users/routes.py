from flask import Blueprint
from flask_mail import Message  # Import Message
import os
import secrets
from flask import render_template, url_for, flash, redirect, request,session
from app import  bcrypt, db
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    )


from app.users.helpers import send_reset_email
from app.helpers import save_picture
from app.users.forms import RegistrationForm,LoginForm,RequestResetForm,ResetPasswordForm,UpdateProfileForm
from app.models import User


users = Blueprint("users", __name__)


# user routes 
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            gender=form.gender.data,
phone_number= form.phone_number.data,
home_address= form.home_address.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("users.login"))
    return render_template("auth/register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("auth/login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user,)
        flash(
            "If this account exists, you will receive an email with instructions","info")
        return redirect(url_for("users.login"))
    return render_template("auth/reset_request.html", title="Reset Password", form = form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])  # Correct route
def reset_password(token):


    user = User.verify_reset_token(token)
    if not user:
        flash("The token is invalid or expired", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated. You can now log in", "success")
        return redirect(url_for("users.login"))
    return render_template("auth/reset_password.html", title="Reset Password", form=form)



@users.route("/view_profile")
@login_required
def view_profile():
    
    return render_template("profile/view_profile.html", title="My Profile")

@users.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, "static/user_pics", output=(150, 150))
            current_user.image_file = picture_file
        current_user.lname = form.lname.data
        current_user.fname = form.fname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.phone_number = form.phone_number.data
        current_user.gender = form.gender.data
        current_user.home_address = form.home_address.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("users.view_profile"))
    elif request.method == "GET":
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.username.data = current_user.username
        form.email.data = current_user.email
        #form.jender.data = current_user.gender
        form.home_address.data = current_user.home_address
        form.phone_number.data = current_user.phone_number
        form.bio.data = current_user.bio
    image_file = url_for("static", filename=f"media/{current_user.image_file}") or url_for('static', filename='default.jpg')
    return render_template("profile/update_profile.html", title="Update My Profile",form = form,image_file=image_file)
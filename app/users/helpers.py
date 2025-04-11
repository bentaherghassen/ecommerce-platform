
from app import  bcrypt, db, mail  # Import mail!! <--------------------
from flask_mail import Message
from flask import url_for
from datetime import datetime
from flask import current_app


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Orca App Password Reset Request",
        sender="YOUR_EMAIL",
        #         sender=app.config.get('MAIL_DEFAULT_SENDER'),  # Use config for sender
        recipients=[user.email],
        body=f"""To reset your password, visit the following link:
        {url_for('reset_password', token=token, _external=True)}
        
        If you did not request a password reset, please ignore this email. Your password will remain unchanged.
        Sincerely,The app_name Team.""",
    )
    mail.send(msg)



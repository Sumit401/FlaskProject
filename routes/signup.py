from flask import Blueprint
import smtplib
from email.message import EmailMessage

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup')
def signup():
    data = smtplib.SMTP("smtp.gmail.com",587)
    data.starttls()
    data.login("sumitsinha401@gmail.com","lykv hsdo nsyb mnrj")
    msg = EmailMessage()
    msg['Subject'] = "OTP from ABC Company"
    msg['From'] = "sumitsinha401@gmail.com"
    msg['To'] = "sumitsinha401@gmail.com"
    msg.set_content("ABC Text")
    print("mail sent")
    data.send_message(msg)
    return 'signup us here'

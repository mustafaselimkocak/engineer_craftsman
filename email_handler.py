import smtplib
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
import streamlit as st

# Function to send an email
def send_email(name: str, email: str, phone: str, pax: str, message: str):

    sender_email = "engineercraftsman@gmail.com"
    sender_password = "efyh kkga xseu csni"

    try:
        # Validate email
        emailinfo = validate_email(email, check_deliverability=False)
        normalized_email = emailinfo.normalized

        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {normalized_email}\nPhone: {phone}\nPAX: {pax}\nMessage: {message}")
        msg['Subject'] = f"New inquiry from {name}"
        msg['From'] = sender_email
        msg['To'] = sender_email  # Send to yourself

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True

    except EmailNotValidError as e:
        st.error("This email address is not valid. Please check your email address.")
        return False

    except Exception as e:
        print(e)
        return False


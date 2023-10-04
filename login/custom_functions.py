from cryptography.fernet import Fernet
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

key = str(config('key'))
key = key.encode()
cipher_suite = Fernet(key)

def gen_encrypted_text(email):
    text = email
    cipher_text = cipher_suite.encrypt(text.encode())
    cipher_text = cipher_text.decode('utf-8')
    return cipher_text


def Validate_Email(email):
    sender_email = config('email')
    sender_password = config('Pass')
    recipient_email = email
    if not sender_email or not sender_password:
        print("Please provide valid sender_email and sender_password.")
        exit(1)

    subject = "Important: Verify Your Account"
    link = f"{config('Dev_Url')}/register/email_validation/{gen_encrypted_text(email)}"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Email body
    body = f"""
    Dear User,

    We are excited to have you join our community. To activate your account, please click the link below:

    Verify Your Account With This Link ({link})

    Thank you for choosing us!

    Best regards,
    Your Support Team
    """
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
    
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    

def Reset_Password(email):

    sender_email = config('email')
    sender_password = config('Pass')
    recipient_email = email
    if not sender_email or not sender_password:
        print("Please provide valid sender_email and sender_password.")
        exit(1)
    subject = "Important: Reset Your Password"
    link = f"{config('Dev_Url')}/register/reset_password_/{gen_encrypted_text(email)}"

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Email body
    body = f"""
    Dear User,

    We are excited to have you join our community. To reset your password, please click the link below:

    Reset Your Password With This Link ({link})

    Thank you for choosing us!

    Best regards,
    Your Support Team
    """
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
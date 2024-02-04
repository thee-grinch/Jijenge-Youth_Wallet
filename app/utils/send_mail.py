
from email.message import EmailMessage
import smtplib
import ssl

def send_mail(receiver: str, link: str, name: str):
    """A function to send email using smtp"""
    email_sender = 'mordecaimuvandi16@gmail.com'
    password = 'rrlxappnhaimwrql'
    email_receiver = receiver

    subject = 'Verify your email'
    body = '''
    Dear {},

Thank you for signing up with [Your Company Name]! To complete the registration process and ensure the security of your account, we kindly ask you to verify your email address.

Please click on the following link to verify your email:
{}

If you are unable to click the link, please copy and paste it into your browser's address bar.

Thank you for choosing Jijenge Youth Group. If you have any questions or need further assistance, please don't hesitate to contact us.

Best regards,
Mordecai Muvandi
Jijenge Youth group Team
    '''.format(name, link)

    em = EmailMessage()
    em['from'] = email_sender
    em['to'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


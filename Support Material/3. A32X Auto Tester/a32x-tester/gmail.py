import smtplib
from email.message import EmailMessage
import ssl

def gmail(subject, outFile):
    # User configuration
    sender_email = 'roldan5150@gmail.com'
    receiver_email = 'roldan5150@gmail.com'
    password = 'Telcontar1015$'
    msg = EmailMessage()

    # Email text
    f = open(outFile, "r")
    msg.set_content(f.read())
    msg['Subject'] = subject
    msg['From'] = "roldan5150@gmail.com"
    msg['To'] = "roldan5150@gmail.com"

    # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Encrypts the email
    context = ssl.create_default_context()
    server.starttls(context=context)
    # We log in into our Google account
    server.login(sender_email, password)
    # Sending email from sender, to receiver with the email body
    server.send_message(msg)
    print('Email sent!')

    #print('Closing the server...')
    server.quit()
    
    return
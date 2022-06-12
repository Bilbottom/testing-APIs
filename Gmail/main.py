"""
Following instructions at
"""

import smtplib
import ssl


if __name__ == '__main__':
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "my@gmail.com"
    password = input("Type your password and press enter: ")

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.quit()
    except Exception as e:
        print(e)

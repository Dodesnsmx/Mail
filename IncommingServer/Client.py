import smtplib
import email.utils
from email.mime.text import MIMEText


if raw_input('Send or receive ? [S/R]') == 'S':

    # Create the message
    msg = MIMEText('This is the body of the message.')
    msg['To'] = email.utils.formataddr(('Recipient', 'arbel03@gmail.com'))
    msg['From'] = email.utils.formataddr(('Author', 'ido@idoar.com'))
    msg['Subject'] = 'Simple test message'
    msg.set_payload('Arbel!')

    server = smtplib.SMTP('127.0.0.1', 1025)
    server.set_debuglevel(True) # show communication with the server
    try:
        server.sendmail(email.utils.parseaddr(msg['From'])[1], email.utils.parseaddr(msg['To'])[1], msg.as_string())
    finally:
        server.quit()


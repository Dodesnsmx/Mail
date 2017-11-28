import smtplib
import email.utils
from email.mime.text import MIMEText
import socket
from IncomingCom import ServerCommunication

if raw_input('Send or receive ? [S/R]') == 'S':

    # Create the message
    msg = MIMEText('This is the body of the message.')
    msg['To'] = email.utils.formataddr(('Recipient', 'ido@idoar.com'))
    msg['From'] = email.utils.formataddr(('Author', 'arbel@idoar.com'))
    msg['Subject'] = 'Simple test message'
    msg.set_payload('Shalom!')

    server = smtplib.SMTP('127.0.0.1', 55555)
    server.set_debuglevel(True) # show communication with the server
    try:
        server.sendmail(email.utils.parseaddr(msg['From'])[1], email.utils.parseaddr(msg['To'])[1], msg.as_string())
    finally:
        server.quit()


else:

    server = ServerCommunication('127.0.0.1', 55555)
    server.connect()
    server.authenticate('ido', '123456')
    print server.fetch(3)
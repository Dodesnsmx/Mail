import smtplib
import email.utils
from email.mime.text import MIMEText
import socket

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

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 110))
    s.send('HELLO')
    d = s.recv(1024)
    if d == 'GOOD CONNECTION':
        s.send('AUTH ido 123')
        d = s.recv(1024)
        if d == 'AUTH SUCCEEDED':
            print 'AUTHORISED!'
            s.send('FETCH 4')
            for i in range(4):
                print 'Receiving...'
                d = s.recv(1024)
                print d
                if d == 'FETCH COMPLETED':
                    break
                s.send('RECEIVED')
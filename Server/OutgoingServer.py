import smtpd
import asyncore
import email
import email.utils as u
import email.generator as g
import os
import smtplib
import time


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        for rcp in rcpttos:
            if rcp.split('@')[1].split('.')[0] == 'idoar':
                self.save_message_to_client(mailfrom, rcp, data)
            else:
                self.relay_message_to_smtp(mailfrom, rcp, data)
        return

    @staticmethod
    def relay_message_to_smtp(mailfrom, rcp, data):
        # Relay the message to the recipient's smtp servr
        # msg = email.message_from_string(data)

        # TODO: DNS parsing of the recipient to get the SMTP server...
        # dom = rcp.split('@')[1].split('.')[0]
        # if dom == 'gmail':
        #     print 'Sending to gmail... (%s)' % rcp
        #     s = smtplib.SMTP('smtp.gmail.com:587')
        # else:
        #     s = smtplib.SMTP('127.0.0.1', 25 )
        # s.set_debuglevel(True)  # show communication with the server
        # try:
        #     s.sendmail(email.utils.parseaddr(msg['From'])[1], email.utils.parseaddr(msg['To'])[1], msg.as_string())
        # finally:
        #     s.quit()
        pass

    @staticmethod
    def save_message_to_client(mailfrom, rcp, data):
        client_name = rcp.split('@')[0]
        client_path = os.getcwd() + '\\Clients\\' + client_name
        if not os.path.exists(client_path):
            os.makedirs(client_path)

        msg = email.message_from_string(data)

        t_stamp = str(time.time()).replace('.', '')

        f_name = client_path + '\\' + t_stamp + '.elm'

        with open(f_name, 'w') as out:
            gen = g.Generator(out)
            gen.flatten(msg)

        return


server = CustomSMTPServer(('127.0.0.1', 55555), None)

print 'SMTP Relay Server binding @(%s, %s)' % server.addr
asyncore.loop()

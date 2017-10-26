# from datetime import datetime
# import asyncore
# from smtpd import SMTPServer
#
#
# class CustomSMTPServer(SMTPServer):
#
#     def process_message(self, peer, mailfrom, rcpttos, data):
#         print 'Message'
#         filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
#                 self.no)
#         f = open(filename, 'w')
#         f.write(data)
#         f.close
#         print '%s saved.' % filename
#         self.no += 1
#
#
#
# def run():
#     server = CustomSMTPServer(('127.0.0.1', 55555), None)
#     try:
#         server
#         asyncore.loop()
#     except KeyboardInterrupt:
#         pass
#
#
# if __name__ == '__main__':
#     run()
#


import smtpd
import asyncore
import email


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
        msg = email.message_from_string(data)
        msg
        return


server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()

from datetime import datetime
import asyncore
from smtpd import SMTPServer


class CustomSMTPServer(SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
                self.no)
        f = open(filename, 'w')
        f.write(data)
        f.close
        print '%s saved.' % filename
        self.no += 1



def run():
    server = CustomSMTPServer(('127.0.0.1', 55555), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()


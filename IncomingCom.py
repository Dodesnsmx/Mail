import socket
import hashlib


class ServerCommunication(object):
    """
    A helper class to simplify communications with the Incoming Mail Server
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_sock = None

    def connect(self):
        """
        Connect to the server.
        :return: None
        """
        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.connect((self.ip, self.port))
            self.server_sock.send('HELLO')
            if self.server_sock.recv(1024) != 'GOOD CONNECTION':
                self.server_sock.shutdown()
                self.server_sock = None
                raise
        except:
            raise Exception('Server did not respond according to protocol, communications terminated.')

    def authenticate(self, un, pw):
        """
        Authenticate yourself to the server.
        :param un: Username
        :param pw: Password
        :return: None
        """

        m = hashlib.md5()
        m.update(pw)

        hashed_pw = m.digest()

        command = 'AUTH ' + un + ' ' + hashed_pw

        try:
            self.server_sock.send(command)
            s = self.server_sock.recv(1024)
            if s != 'AUTH SUCCEEDED':
                raise
        except:
            raise Exception('Authentication Failed. Wrong username or password...')

    def fetch(self, last_time_stamp):
        """
        Fetch all mails that have been received since last mail.
        :param last_time_stamp: last mail's time stamp.
        :return: Mail list by MIME format (string list).
        """
        mails = []
        command = 'FETCH', last_time_stamp
        flag = None
        count_received = 0

        try:
            self.server_sock.send(command)
            while True:
                mail = self.server_sock.recv(10 * 1024)
                if mail.split()[0] == 'FETCHCOMPLETED':
                    flag = mail
                    break
                count_received += 1
                mails.append(mail)
            if flag.split()[1] != str(count_received):
                raise
        except:
            raise Exception('Fetching did not succeed... Try again...')

        return mails

    def disconnect(self):
        """
        Disconnect from server.
        :return: None
        """
        self.server_sock.send('DISCONNECT')
        self.server_sock.recv()


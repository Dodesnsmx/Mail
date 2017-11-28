import socket
import threading
import os


class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = HandleClient, args = (client,address)).start()


class HandleClient(object):

    class ClientState():
        Connected = 1
        Authorized = 2
        FetchRequested = 3
        FetchSucceeded = 4
        FetchFailed = 5
        DelRequested = 6
        DelSucceeded = 7
        DelFailed = 8
        Disconnected = 9

    def __init__(self, cli_sock, addr):
        self.address = addr
        self.socket = cli_sock
        self.client_state = self.ClientState.Disconnected
        self.last_mail_fetched_index = 0
        self.conversation_loop()

    def conversation_loop(self):
        size = 1024
        while True:
            try:
                data = self.socket.recv(size)
                if data:
                    if data.upper() == 'HELLO':
                        self.client_state = self.ClientState.Connected
                        self.socket.send('GOOD CONNECTION')
                    elif data.split(' ')[0].upper() == 'AUTH':
                        self.username = data.split(' ')[1]
                        pw = data.split(' ')[2]
                        # TODO: Authorisation Process...
                        self.client_state = self.ClientState.Authorized
                        self.socket.send('AUTH SUCCEEDED')
                        # OR self.socket.send('AUTH FAILED')
                    elif data.split(' ')[0].upper() == 'FETCH':
                        fetch_amount_req = data.split(' ')[1]
                        client_mails_path = os.getcwd() + '\\clients\\' + self.username
                        mail_file_names = []
                        for (dirpath, dirnames, filenames) in os.walk(client_mails_path):
                            mail_file_names.extend(filenames)
                            break

                        fetch_amount = min([fetch_amount_req, len(mail_file_names)])
                        for i in range(fetch_amount):
                            f = open(client_mails_path + '\\' + mail_file_names[i], 'r')
                            self.socket.send(f.read())
                            self.socket.recv(1024)
                        self.socket.send('FETCHCOMPLETED ' + str(fetch_amount), 'SENT')

                else:
                    raise
            except:
                self.client_state = self.ClientState.Disconnected
                self.socket.close()
                return False


if __name__ == "__main__":
    Server('127.0.0.1', 55555).listen()
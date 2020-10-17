from threading import Thread
import socket
import os

HOST = 'localhost'
PORT = 1060

class Server(Thread):
    def __init__(self):
        super().__init__()
        self.host = '127.0.0.1'
        self.port = 1060
        self.clients = []
        self.usernames = dict()
    
    def run(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # this part is new info; i think we should ask Christine's advice on whether to use
        # but it essentially allows us to use an old port without waiting
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        serverSocket.bind((HOST, PORT))

        # this listening socket only establishes TCP connections. We handle the connecting to threads in the clientThread class
        serverSocket.listen(1)
        print('Waiting for client connections at', HOST)

        # Create threads for each client that connects
        while True:
            connection, address = serverSocket.accept()
            print('Client connected') #add which client connected to

            # create thread for client
            new_client_thread = ClientThread(connection, address, self)

            self.check_username(new_client_thread)
            self.broadcast('Server: {} has joined the chat. Say hi!'.format(new_client_thread.name), new_client_thread)

            # begin the new thread
            new_client_thread.start()


            # add thread to active connections 
            self.clients.append(new_client_thread)
            print('Ready to receive messages from', connection.getpeername(), new_client_thread.name)

    def check_username(self, client):
        client.send('Server: Please enter a username. ')
        username = client.connection.recv(1024).decode('ascii')
        while username in self.usernames.keys():
            client.send('Server: Username taken. Please enter a new username: ')
            username = client.connection.recv(1024).decode('ascii')
        self.usernames[username] = client
        client.name = username
        client.send('Server: Welcome to the chat! Your username is {}.'.format(client.name))


    def broadcast(self, message, source):
        for client in self.clients:
            if client.address != source:
                client.send(message)
    
    def remove_client(self, client):
        self.clients.remove(client)
        self.usernames.pop(client.name, None)

class ClientThread(Thread):
    def __init__(self, connection, address, server):
        super().__init__()
        self.connection = connection
        self.address = address
        self.server = server
        self.name = None
    
    def run(self):
        while True:

            try:
                message = self.connection.recv(1024).decode('ascii')
            except:
                # user has "quit" the chat room, so we need to exit the thread
                print('{} has left the chat room'.format(self.name))
                self.server.broadcast('Server: {} has just left the chat.'.format(self.name), self.address)
                self.connection.close()
                server.remove_client(self)
                return
            
            if (message[0] == '+'):
                try:
                    username, message = message[1:].split(' ', 1)
                    # prepend message to show it was a private message from another user
                    message = '(private) ' + self.name + ': ' + message
                    print(self.address, ': ', message)
                    try:
                        server.usernames.get(username, None).send(message)
                    except:
                        self.send('Server: User \'{}\' not found'.format(username))
                except:
                    continue
            
            elif (message.lower() == 'list'):
                names = 'List of users in the chatroom:\n'
                for username in server.usernames.keys():
                    names += '- ' + username + '\n'
                self.send(names)
            else:
                # prepend message with the client's name to show where it came from
                message = self.name + ': ' + message
                print(self.address, ': ', message)
                self.server.broadcast(message, self.address)
                       
    
    def send(self, message):
        self.connection.sendall(message.encode('ascii'))

def closeServer(server):
    while True:
        x = input()
        if x == 'q':
            # close all connections
            for client in server.clients:
                client.connection.close()
            os._exit(0)

if __name__ == '__main__':
    server = Server()
    server.start()

    closeServer = Thread(target=closeServer, args=(server,))
    closeServer.start()
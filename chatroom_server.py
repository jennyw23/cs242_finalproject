from threading import Thread
import socket

HOST = 'localhost'
PORT = 1060

class Server(Thread):
    def __init__(self):
        super().__init__()
        self.host = '127.0.0.1'
        self.port = 1060
        self.clients = []
    
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

            # begin the new thread
            new_client_thread.start()

            # add thread to active connections 
            self.clients.append(new_client_thread)
            print('Ready to receive messages from', connection.getpeername())


    def broadcast(self, message, source):
        for client in self.clients:
            if client.address != source:
                client.send(message)
    
    def remove_client(self, client):
        self.clients.remove(client)

class ClientThread(Thread):
    def __init__(self, connection, address, server):
        super().__init__()
        self.connection = connection
        self.address = address
        self.server = server
    
    def run(self):
        while True:
            
            message = self.connection.recv(1024).decode('ascii')

            if message != "":
                print(self.address, ': ', message)
                self.server.broadcast(message, self.address)
            else:
                # user has "quit" the chat room, so we need to exit the thread
                print('{} has left the chat room'.format(self.address))
                self.connection.close()
                server.remove_client(self)
                return       
    
    def send(self, message):
        self.connection.sendall(message.encode('ascii'))

if __name__ == '__main__':
    server = Server()
    server.start()
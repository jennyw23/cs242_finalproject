import threading
import socket
import argparse
import os

terriIP = 'localhost'
terriHOST = '192.168.8.104'

class Send(threading.Thread):
    """
    This class listens for user input from the command line.
    """
    def __init__(self, sock):
        """
        Initialize instance variables.
        sock: The socket object to be connected
        name: Inputted username
        """
        super().__init__()
        self.sock = sock
        # self.name = name

    def run(self):
        """
        Takes user input (from command line) and sends to the server
        Typing 'QUIT' closes connection between client and server
        """
        while True:
            # message = input('{}: '.format(self.name))
            message = input()

            # Type 'QUIT' to leave the chatroom
            if message.upper() == 'QUIT':
                self.sock.sendall('Server: {} has just left the chat.'.format(self.name).encode('ascii'))
                break
            
            # Send message to server for broadcasting
            else:
                # self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))
                self.sock.sendall(message.encode('ascii'))
        
        print('\nQuitting...')
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
    """
    This class listens for incoming messages from the server.
    """
    def __init__(self, sock):
        """
        Initialize instance variables.
        sock: The socket object to be connected
        name: Inputted username
        """
        super().__init__()
        self.sock = sock
        # self.name = name

    def run(self):
        """
        Receives data from the server and prints in terminal. 
        Note that stops listening for incoming data when either end has closed socket.
        """
        while True:
            message = self.sock.recv(1024).decode('ascii')

            if message:
                # print('\r{}\n{}: '.format(message, self.name), end = '')
                print(message)
            
            else:
                # Server has closed the socket, exit the program
                print('\nOh no, we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

class Client:
    """
    This class creates a client object
    """
    def __init__(self, host, port):
        """
        host: The IP address of the server's listening socket.
        port: The port number of the server's listening socket.
        sock: The connected socket object.
        name: The username of the client.
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
    
    def start(self):
        """
        Creates client-server connection. 
        Records username from user input.
        Creates and starts the Send and Receive threads.
        Notifies other connected clients client has just entered chatroom.
        Returns: A Receive object representing the receiving thread.
        """
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))
        
        # print()
        # self.name = input('Please input your screen name: ')

        # print()
        # print('Welcome, {}!'.format(self.name))

        # Create send and receive threads
        send = Send(self.sock)
        receive = Receive(self.sock)

        # Start send and receive threads
        send.start()
        receive.start()

        # self.sock.sendall('Server: {} has joined the chat. Say hi!'.format(self.name).encode('ascii'))
        print("\rYou're now ready to send and receive messages! To leave the chatroom, type 'QUIT'\n")
        # print('{}: '.format(self.name), end = '')

        return receive


def main(host, port):
    """
    Initializes and runs the GUI application.
    host: The IP address of the server's listening socket.
    port: The port number of the server's listening socket.
    """
    client = Client(host, port)
    receive = client.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    main(args.host, args.p)
import threading
import socket

HOST = 'localhost'
PORT = 1060

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(HOST, PORT)
socket.listen()
print('Waiting for client connections')

while True:
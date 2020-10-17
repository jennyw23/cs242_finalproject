# cs242_finalproject

# Team members: Diego Berny, Eden Liu, Terri Liu, Jenny Wang


Our chat room protocol contains two files: client.py and chatroom_server.py.

Pre-Working GUI Version:

***The chat room server has a variable called 'HOST' that is currently hardcoded with 'localhost'. The application currently runs on the local computer. If time permits, we'll explore using multiple IPs on the same LAN

1) Open Terminal
2) Run the chatroom_server.py file using Python3 
3) 'Waiting for client connections at localhost' should be displayed.
4) Open a new Terminal Window
5) Run the client.py file using Python3. It will require a host argument which we've set to localhost (the server is running on the local machine). Thus, type "python3 client.py localhost" in the command line.
6) You should now be prompted for a username. Enter a username.
7) Open multiple termainl windows and follow steps 5-6 to chat with other clients.

Features:
- type "+<username>" to private message a specific person.
- type "list" (no whitespaces) to list the other users in the chat room

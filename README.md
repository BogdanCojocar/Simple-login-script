Application written in python 2.7

Server should be started first. A list of users and their passwords is managed by the server. New users can be added.
Multiple clients can connect to the server. If the user_name or password which is entered by the client is not found on the server, he is rejected.
The comunication between the server and the client is done using sockets. The password is encrypted using the AES algorithm.
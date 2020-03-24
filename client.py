import socket
        
from threading import Thread

HOST = '127.0.0.1'
PORT = 5000
BUFF_SIZE = 1024    


# Create a socket in the specified domain and of the specified type.
### AF_INET is reference to th the domain, it means ipv4
### SOCK_STREAM it refers to a TCP socket, which is our type of socket. 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


client_socket.connect((HOST , PORT))

# receive welcome message 
msg = client_socket.recv(BUFF_SIZE).decode("utf-8") 
print(msg)

name = input("Enter your name : ")
name = name.encode("utf-8")

# send name 
client_socket.send(name) 

# receive  second welcome message 
msg = client_socket.recv(BUFF_SIZE).decode("utf-8") 
print(msg)

def clientSend():
    try:
        while 1 :
            msg = input('me:- ')
            msg = msg.encode('utf-8')
            client_socket.send(msg)
              
    except : 
        print('Error')
        client_socket.close()
        return
        

t = Thread(target = clientSend)
t.start()  

import sys   

try:
    while True:
        recv_msg = client_socket.recv(BUFF_SIZE)
        recv_msg = recv_msg.decode('utf-8')
        if msg != "{quite}" : 
             print( '\n' , recv_msg)
        # recv 'quite' to close 
        else:
            print("I left chat")
            break
except: 
    print()
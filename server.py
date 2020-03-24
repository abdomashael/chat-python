import socket

from threading import Thread
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

HOST = '127.0.0.1'
PORT = 5000
BUFF_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()
BUFF_SIZE = 1024

key = RSA.generate(2048)
public_key = key.publickey().export_key(format='PEM', passphrase=None, pkcs=1)

print(f'Listening for connections on {HOST}:{PORT}...')

clients = {}
clients_keys = {}


def accept_connections():
    while True:
        con, add = server_socket.accept()
        print('{} has entered chat'.format(add[1]))

        con.send(public_key)
        clinet_rec = con.recv(BUFF_SIZE)
        clinet_rec = bytearray(clinet_rec)
        clinet_rec = bytes(clinet_rec)

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(key)
        session_key = cipher_rsa.decrypt(clinet_rec)
        clients_keys[con] = session_key
        con.send("Welcome to Fathi Chat, plz enter name ".encode('utf-8'))
        Thread(target=handleClient, args=[con, ]).start()  # start thread to handle client


def handleClient(con):
    name = con.recv(1024)
    name = name.decode("utf-8")
    print(name)
    msg = "welcome " + name + " write {quite} to exit form chat"
    con.send(msg.encode("utf-8"))
    clients[con] = con
    sendToAll("{} has entered chat".format(name), "", con1=con)
    try:
        while 1:
            msg = con.recv(BUFF_SIZE)
            msg = msg.decode('utf-8')
            print(name, msg, sep=":")
            if msg != "{quite}":
                sendToAll(msg, name, con1=con)
            else:
                con.send("{quite}".encode("utf-8"))
                del clients[con]  # remove from set
                sendToAll(" {} has left chat".format(name), "", con1=None)
                con.close()
                break
    except:
        sendToAll(" {} has left chat".format(name), "", con1=None)


def sendToAll(msg, src, con1):  # keep track of no-defaut must be last
    src = src + "::" + msg
    msg = msg.encode("utf-8")
    for con in clients:
        key=clients_keys[con]
        if con != con1:
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext = cipher.encrypt(msg)
            con.send(bytearray(ciphertext))
            print(bytearray(ciphertext))


t = Thread(target=accept_connections)
t.start()
t.join()

import socket
from hashlib import md5

def send(socket, msg):
    length = str(len(str(msg)))
    msg = length + '!' + str(msg)
    socket.send(msg.encode())

def recv(socket):
    num = ''
    while '!' not in num:
        num += socket.recv(1).decode()
    num = num.replace('!', '')
    if not num.isnumeric():
        print('Protocol could not find length')
        return 1  # Protocol could not find length
    
    num = int(num)
    return socket.recv(num).decode()

def md5_hash(s):
    return md5(s.encode()).hexdigest()

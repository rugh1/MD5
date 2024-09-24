#rugh1
#24.9.24
#client for distributed MD5 brute force
import hashlib
import socket
import threading

IP = '127.0.0.1'
PORT = 25566

def recv(socket):
    num = ''
    while '!' not in num:
        socket.recv(1).decode()
    num[:-1]
    if(not num.isnumeric()):
        print('protocol couldnt find length')
        return 1 #protocol couldnt find length
    
    num = int(num)
    str = socket.recv(num).decode()
    return str


def send(socket, msg):
    length = str(len(msg))
    msg = length + '!' + msg
    socket.send(msg.encode())


def md5_hash(str):
    return(hashlib.md5(str.encode()).hexdigest())


def run_thread(min, max, target):
    print(min, max)
    for i in range(min, max):
        if md5_hash(str(i)).upper() == (target):
                print(f"found {i}")
                return(i)
    return(0)


def main():
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try:
    #     num_of_cores = 0
    #     client_socket.connect((IP,PORT))
    #     send(num_of_cores)
    #     range = recv(client_socket)

    # except socket.error():
    #     print("client socket incounterd errors")
    amount_each_jump = 10000000 #recv from server means how much numbers each thread does until updates server 
    num_of_cores = 8
    min = 0 #recv from server
    max = 9999999999 #recv from server

    while(min < max):
        for i in range(num_of_cores):
            thread = threading.Thread(target = run_thread, args = (min,min + amount_each_jump, 'EC9C0F7EDCC18A98B1F31853B1813301'))
            thread.start()
            min += amount_each_jump
if __name__ == '__main__':
    main()
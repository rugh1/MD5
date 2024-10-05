"""
author: rugh1
date: 05/10/24
description: server for md5 project built on nir dweck's simple multi-threaded TCP server 
"""
import socket
from threading import Thread
from threading import Lock
from hashlib import md5
from extras import send, recv, md5_hash

RANGE_QUEUE = []
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
FOUND = 'No'
TARGET = '9f3e4277d7cc6ec0f3e82bf75d359801'
MIN_RANGE = 0
MAX_RANGE = 400000000
CHUNK_SIZE = 10000000
lock = Lock()

def create_range_queue(start, end, chunk_size):
    """
    Creates a queue of smaller ranges from a larger range.
    
    Args:
    start (int): The start of the large range.
    end (int): The end of the large range.
    chunk_size (int): The size of each smaller range.
    
    Returns:
    deque: A queue of tuples, each containing (start, end) of a smaller range.
    """
    current = start
    
    while current < end:
        range_start = current
        range_end = min(current + chunk_size - 1, end)
        RANGE_QUEUE.append((f'{range_start}-{range_end}'))
        current = range_end + 1

def handle_connection(client_socket, client_address):
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
    try:
        global FOUND
        global lock 
        print("got connection")
        num_of_cores = int(recv(client_socket))
        print(num_of_cores)
        send(client_socket, TARGET)
        current_range = None  # New: Initialize current_range
        while len(RANGE_QUEUE) > 0 and FOUND == 'No':
            lock.acquire()
            print(len(RANGE_QUEUE))
            if len(RANGE_QUEUE) == 0: 
                break
            current_range = RANGE_QUEUE.pop()
            lock.release()
            send(client_socket, current_range)
            result = recv(client_socket)
            if result.split(':')[1] != 'No':
                num = int(result.split(':')[1])
                if md5_hash(str(num)) == (TARGET.lower()):
                    FOUND = result
                    print(f'found:{FOUND}')
        print('closing')
        send(client_socket, 'DONE')
    except socket.error as err:
        print('received socket exception - ' + str(err))
        if current_range:
            RANGE_QUEUE.append(current_range)
    finally:
        client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    create_range_queue(MIN_RANGE, MAX_RANGE, CHUNK_SIZE)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        global FOUND
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        
        while FOUND == 'No':
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_connection,
                            args=(client_socket, client_address))
            thread.start()
        print(FOUND)
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
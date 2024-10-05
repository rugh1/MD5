"""
author: rugh1
date: 05/10/24
description: server for md5 project built on nir dweck's simple multithreaded TCP server
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
    
    :param start: The start of the large range
    :type start: int
    :param end: The end of the large range
    :type end: int
    :param chunk_size: The size of each smaller range
    :type chunk_size: int
    :return: None
    """
    global RANGE_QUEUE
    RANGE_QUEUE = []
    current = start

    while current < end:
        range_start = current
        range_end = min(current + chunk_size - 1, end)
        RANGE_QUEUE.append(f'{range_start}-{range_end}')
        current = range_end + 1


def handle_connection(client_socket, client_address):
    """
    Handle a client connection.

    :param client_socket: The connection socket    :type client_socket: .socket
    :param client_address: The remote address
    :type client_address: tuple
    :return: None
    """
    try:
        current_range = None  # New: Initialize current_range
        global FOUND
        global lock
        print(f"got connection {client_address}")
        num_of_cores = int(recv(client_socket))
        print(num_of_cores)
        send(client_socket, TARGET)
        while len(RANGE_QUEUE) > 0 and FOUND == 'No':
            lock.acquire()
            print(len(RANGE_QUEUE))
            if len(RANGE_QUEUE) == 0:
                lock.release()
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
    """
    Main function to set up the server and handle client connections.

    This function creates the range queue, sets up the server socket,
    and continuously accepts new client connections, spawning a new thread for each.

    :return: None
    """
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
     # Test create_range_queue function
    print("Testing create_range_queue function:")
    
    # Test case 1: Small range
    create_range_queue(0, 100, 30)
    expected_queue_1 = ['0-29', '30-59', '60-89', '90-100']
    assert RANGE_QUEUE == expected_queue_1, f"Test case 1 failed. Expected {expected_queue_1}, but got {RANGE_QUEUE}"
    print("Test case 1 passed.")

    # Test case 2: Larger range
    create_range_queue(1000, 5000, 1000)
    expected_queue_2 = ['1000-1999', '2000-2999', '3000-3999', '4000-4999']
    assert RANGE_QUEUE == expected_queue_2, f"Test case 2 failed. Expected {expected_queue_2}, but got {RANGE_QUEUE}"
    print("Test case 2 passed.")

    # Test case 3: Range smaller than chunk size
    create_range_queue(0, 50, 100)
    expected_queue_3 = ['0-50']
    assert RANGE_QUEUE == expected_queue_3, f"Test case 3 failed. Expected {expected_queue_3}, but got {RANGE_QUEUE}"
    print("Test case 3 passed.")

    print("All test cases for create_range_queue passed successfully.")

    main()

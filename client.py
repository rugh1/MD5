# rugh1
# 24.9.24
# client for distributed MD5 brute force
from concurrent.futures import ThreadPoolExecutor
import hashlib
import socket
import threading
import os
from extras import send, recv, md5_hash

IP = '127.0.0.1'
PORT = 8080
FOUND = 'No'


def run_thread(min, max, target):
    """
    Run a thread to check a range of numbers for MD5 hash match.

    :param min: The minimum number in the range to check
    :type min: int
    :param max: The maximum number in the range to check
    :type max: int
    :param target: The target MD5 hash to match
    :type target: str
    :return: None
    """
    global FOUND
    print('start', min, max)
    for i in range(min, max):
        if md5_hash(str(i)) == (target.lower()):
            print(f"found {i}")  # print found number
            FOUND = i


def main():
    """
    Main function to handle client operations.

    This function establishes a connection with the server, receives tasks,
    and coordinates the multithreaded hash cracking process.

    :return: None
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        num_of_cores = os.cpu_count()
        print("hi")
        client_socket.connect((IP, PORT))
        print("hello")
        send(client_socket, num_of_cores)
        target = recv(client_socket)
        while FOUND == 'No':
            range = recv(client_socket)
            print(range)
            if range == 'DONE':
                break
            min_val, max_val = map(int, range.split('-'))
            amount_each_jump = int((max_val - min_val) / num_of_cores)
            with ThreadPoolExecutor(max_workers=num_of_cores) as executor:
                while min_val < max_val:
                    executor.submit(run_thread, min_val, min(min_val + amount_each_jump, max_val), target)
                    min_val += amount_each_jump
            send(client_socket, f"{min_val}-{max_val}:{FOUND}")
            print(FOUND)

    except socket.error as e:
        print(f"client socket encountered errors {e}")


if __name__ == '__main__':
    main()

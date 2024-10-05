"""
Utility functions for network communication and hashing.

This module provides helper functions for sending and receiving messages over sockets,
as well as a function for computing MD5 hashes.

Author: rugh1
Date: 05/10/24
"""

import socket
from hashlib import md5


def send(socket, msg):
    """
    Send a message over a socket with a length prefix.

    :param socket: The socket to send the message through
    :type socket: socket.socket
    :param msg: The message to send
    :type msg: str or any type that can be converted to str
    :return: None
    """
    length = str(len(str(msg)))
    msg = length + '!' + str(msg)
    socket.send(msg.encode())


def recv(socket):
    """
    Receive a message from a socket with a length prefix.

    :param socket: The socket to receive the message from
    :type socket: socket.socket
    :return: The received message as a string, or 1 if an error occurred
    :rtype: str or int
    """
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
    """
    Compute the MD5 hash of a string.

    :param s: The string to hash
    :type s: str
    :return: The MD5 hash of the input string as a hexadecimal string
    :rtype: str
    """
    return md5(s.encode()).hexdigest()

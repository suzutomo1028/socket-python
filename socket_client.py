#!/usr/bin/env python3

""" クライアント """

import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG, \
    format='%(levelname)s : %(threadName)s : %(module)s : %(funcName)s : %(message)s')

class SocketClient:

    def __init__(self, addr:str, port: int) -> None:
        self.addr: str = addr
        self.port: int = port

    def run(self) -> None:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.addr, self.port))

            server_addr = client.getpeername()
            logging.debug('Client connected server - server %s', server_addr)

            while True:
                line = input('> ')

                if not line:
                    continue
                elif line == 'quit':
                    break
                else:
                    data = line.encode('utf-8')
                    client.send(data)
                    logging.debug('Client sent data - %s', data)

                    data = client.recv(1024)
                    logging.debug('Client received data - %s', data)

        except ConnectionError as e:
            print(e)

        finally:
            client_addr = client.getsockname()
            client.close()
            logging.debug('Client closed - client %s', client_addr)

if __name__ == '__main__':
    client = SocketClient('localhost', 8888)
    client.run()

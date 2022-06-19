#!/usr/bin/env python3

""" サーバ """

import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG, \
    format='%(levelname)s : %(threadName)s : %(module)s : %(funcName)s : %(message)s')

class SocketServer:

    def __init__(self, address: str, port: int) -> None:
        self.addr: str = address
        self.port: int = port
        self.is_running: bool = False

    def run(self) -> None:
        if self.is_running:
            logging.debug('Server is already running')
            return

        self.is_running = True

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(0.5)
            server.bind((self.addr, self.port))
            server.listen()

            server_addr = server.getsockname()
            logging.debug('Server started accepting - server %s', server_addr)

            while True:
                try:
                    (client, client_addr) = server.accept()
                    logging.debug('Server accepted client - client %s', client_addr)
                except socket.timeout:
                    continue

                thread = threading.Thread(target=self.worker, args=(client,))
                thread.daemon = True
                thread.start()

        except KeyboardInterrupt:
            self.is_running = False

            for thread in threading.enumerate():
                if thread is threading.current_thread():
                    continue
                thread.join()

        finally:
            server.close()
            logging.debug('Server closed - server %s', server_addr)

    def worker(self, client: socket.socket) -> None:
        if client is not None:
            client.settimeout(0.5)
            client_addr = client.getpeername()

            while self.is_running:
                try:
                    data = client.recv(1024)
                    logging.debug('Server received data - %s', data)
                except socket.timeout:
                    continue

                if not data:
                    logging.debug('Client disconnected - client %s', client_addr)
                    break

                client.send(data)
                logging.debug('Server sent data - %s', data)

            client.close()
            logging.debug('Server closed - client %s', client_addr)

if __name__ == '__main__':
    server = SocketServer('localhost', 8888)
    server.run()


import os
import sys
import time
import logging
import threading

path = os.path.dirname(os.path.realpath(__file__))[:-7]
if path not in sys.path:
    sys.path.append(path)


from common.sock_listener import Sock_listener
from common.settings import Settings
from connection import Connection
from games import Games


class Server():
    
    def __init__(self):
        logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
        self._keep_running = True
        self._games = Games()

        
    def run(self):
        while self._keep_running:
            start_time = time.time()
            self._games.tick()
            sleep_time = Settings.TICK - (time.time() - start_time)
            if sleep_time > 0.001:
                time.sleep(sleep_time)
    
    
    def stop(self):
        self._keep_running = False


server = Server()

listener = Sock_listener(Settings.SERVER_HOST, Settings.PORT, Connection)

thread = threading.Thread(target=listener.run)
thread.daemon = True
thread.start()

try:
    server.run()
except KeyboardInterrupt:
    pass

listener.stop()
server.stop()

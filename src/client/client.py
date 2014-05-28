

import os
import sys
import time

path = os.path.dirname(os.path.realpath(__file__))[:-7]
if path not in sys.path:
    sys.path.append(path)


from connection import Connection
from game import Game


class Client():
    
    def __init__(self, is_bot):
        self._game =  Game(is_bot)
    
        
    def run(self):
        self._game.get_connection_address()
        self._game.set_text('Connecting to server...')
        
        connection = Connection(self._game)
        self._game.set_connection(connection)
        
        connection.poll(30, 1)
 
        if connection.connected:
            self._game.set_text('Connected to server')
        else:
            self._game.set_text('Failed to connect to server, closing...')
            time.sleep(2)
            return

        self._game.run()
        
        self._game.set_text('Disconnected from server, closing...')
        time.sleep(1)


    def stop(self):
        self._game.stop()
        

if __name__ == '__main__':
    is_bot = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'True':
            is_bot = True
    
    client = Client(is_bot)
    client.run()

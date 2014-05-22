

import os
import sys
import time

path = os.path.dirname(os.path.realpath(__file__))[:-7]
if path not in sys.path:
    sys.path.append(path)


from connection import Connection
from game import Game


game = Game()
game.get_connection_address()
game.set_text('Connecting to server...')

connection = Connection(game)
game.set_connection(connection)

connection.poll(30, 1)
 
if connection.connected:
    game.set_text('Connected to server')
else:
    game.set_text('Failed to connect to server, closing...')
    time.sleep(2)
    exit()

game.run()

game.set_text('Disconnected from server, closing...')
time.sleep(1)

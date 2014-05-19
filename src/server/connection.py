
from common.sock_connection import Sock_connection

from connections import Connections


class Connection(Sock_connection):
    
    def __init__(self, sock):
        Sock_connection.__init__(self, sock=sock)
        self._connections = Connections()
        self._game = None
        self._connection_number = None
    
    
    def on_accept(self):
        self._connections.add_connection(self)
    
    
    def on_close(self):
        if self._connection_number is None:
            # Note: if this does get printed, should look into doing something besides printing it out
            print 'look into why this has no connection number'
            return
        self._connections.close_connection(self._connection_number)
        self._game = None
    
    
    def on_message(self, message):
        if self._game is None:
            return
        self._game.message(message, self._connection_number)
    
        
    def set_connection_number(self, number):
        self._connection_number = number
        
    
    def get_connection_number(self):
        return self._connection_number
    
    
    def set_game(self, game):
        self._game = game


    def get_game(self):
        return self._game

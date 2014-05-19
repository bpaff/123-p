
from common.sock_connection import Sock_connection
from common.settings import Settings


class Connection(Sock_connection):
    
    def __init__(self, game):
        self._game = game
        host = game.get_connection_host()
        if host is None:
            self.connected = False
            return
        Sock_connection.__init__(self, host, Settings.PORT)
    
    
    def on_close(self):
        self._game.stop()
    
        
    def on_message(self, message):
        self._game.message(message)

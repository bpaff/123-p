
from common.singleton import Singleton


class Connections(Singleton):
    
    def __init__(self):
        self._connection_number = 0
        self._connections = {}
        self._new_connections = []
    
    
    def _get_next_connection_number(self):
        self._connection_number += 1
        while self._connection_number in self._connections:
            self._connection_number += 1
            if self._connection_number > 999999999:
                self._connection_number = 1
        return self._connection_number
    
    
    def add_connection(self, connection):
        connection_number = self._get_next_connection_number()
        self._connections[connection_number] = connection
        connection.set_connection_number(connection_number)
        self._new_connections.append(connection)
    
    
    def get_new_connection_and_remove(self):
        if self._new_connections:
            return self._new_connections.pop()
        return None


    def close_connection(self, connection_number):
        connection = self._connections.get(connection_number, None)
        if connection is None:
            return
        game = connection.get_game()
        if game is not None:
            game.drop_connection(connection_number)
        del self._connections[connection_number]

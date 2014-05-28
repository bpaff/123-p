
from common.singleton import Singleton


class Connections(Singleton):
    
    def __init__(self):
        self._connection_number = 0
        self._connections = {}
        self._connections_looking = []
    
    
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
    
    
    def get_connection_looking_and_remove(self):
        if self._connections_looking:
            return self._connections_looking.pop()
        return None
    
    
    def looking_for_game(self, connection):
        self._connections_looking.append(connection)


    def close_connection(self, connection_number):
        connection = self._connections.get(connection_number, None)
        if connection is None:
            return
        game = connection.get_game()
        if game is not None:
            game.drop_connection(connection_number)
        del self._connections[connection_number]


from connections import Connections
from game import Game
from common.settings import Settings


class Games():
    
    def __init__(self):
        self._connections = Connections()
        self._connections_need_game = []
        self._number_of_wait_ticks = 0
        self._game_number = 0
        self._games = {}
        self._games_to_kill = []
    
    
    def _get_next_game_number(self):
        self._game_number += 1
        while self._game_number in self._games:
            self._game_number += 1
            if self._game_number > 999999999:
                self._game_number = 1
        return self._game_number
    
    
    def tick(self):
        self._kill_games()
        self._get_new_connections()
        self._do_matchmaking()
        self._tick_games()
    
    
    def _kill_games(self):
        while self._games_to_kill:
            game = self._games_to_kill.pop()
            game_number = game.get_game_number()
            if game_number in self._games: 
                game.end_game()
                self._connections_need_game.extend(game.get_connections().itervalues())
                del self._games[game_number]
    
    
    def _get_new_connections(self):
        while True:
            connection = self._connections.get_new_connection_and_remove()
            if connection == None:
                return
            self._connections_need_game.append(connection)
    
    
    def _do_matchmaking(self):
        if not self._connections_need_game:
            return
        
        for i in range(len(self._connections_need_game) - 1, -1, -1):
            if not self._connections_need_game[i].connected:
                self._connections_need_game.pop(i)
                
        if (
            self._number_of_wait_ticks > Settings.MATCHMAKER_WAIT_TICKS 
            or len(self._connections_need_game) >= Settings.MATCHMAKER_MAXIMUM_PLAYERS
        ):
            self._create_game()
            self._number_of_wait_ticks = 0
            return
        
        self._number_of_wait_ticks += 1
    
    
    def _create_game(self):
        game_number = self._get_next_game_number()
        game = Game(self, game_number)
        self._games[game_number] = game
        
        count = 0
        while self._connections_need_game:
            game.add_connection(self._connections_need_game.pop())
            count += 1
            if count >= Settings.MATCHMAKER_MAXIMUM_PLAYERS:
                break
            
        game.start_game()
        
    
    def _tick_games(self):
        if not self._games:
            return
        
        for game in self._games.itervalues():
            if game.get_game_over():
                self._games_to_kill.append(game)
            else:
                game.tick()

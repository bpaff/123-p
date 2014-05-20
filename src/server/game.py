
import time
import json
import logging

from ai import Ai
from common.settings import Settings
from common.messages import Messages
from common.light_cycle import Light_cycle


class Game():
    
    def __init__(self, games, game_number):
        self._games = games
        self._game_number = game_number
        self._connections = {}
        self._connections_message_to_receive = {}
        self._connection_to_drop = []
        self._connection_to_cycle = {}
        self._light_cycles = {}
        self._light_cycles_ai = {}
        self._dead_cycles = []
        self._game_over = False
        self._tick_number = 1
        self._last_tick_time = None
        self._messages = []
        self._message_history_tick = 0
        self._message_history = {}
        self._waiting_for_startup = True
        self._waiting_for_startup_ticks = 0
    
    
    def add_connection(self, connection):
        connection_number = connection.get_connection_number()
        self._connections[connection_number] = connection
        self._connections_message_to_receive[connection_number] = []
        connection.set_game(self)
    
    
    def drop_connection(self, connection_number):
        if connection_number in self._connections:
            self._connection_to_drop.append(connection_number)
        
    
    def start_game(self):   
        logging.debug('start_game, _game_number: ' + str(self._game_number))
        for key in self._connections:
            if not self._connections[key].connected:
                self._connection_to_drop.append(self._connections[key].get_connection_number())
        self._cleanup_dropped_connections()
        if self._game_over:
            return
        self._create_light_cycles()
        self._last_tick_time = time.time()
    
    
    def _cleanup_dropped_connections(self):
        while self._connection_to_drop:
            connection_number = self._connection_to_drop.pop()
            if connection_number in self._connections:
                del self._connections[connection_number]
                del self._connections_message_to_receive[connection_number]
            if self._light_cycles == {}:
                break
            cycle_number = self._connection_to_cycle.get(connection_number, None)
            if cycle_number is None:
                break
            self._light_cycles_ai[cycle_number] = Ai(self._light_cycles, cycle_number)
        
        if not self._connections:
            self.end_game()
        
    
    def _create_light_cycles(self):
        count = 0
        for key in self._connections:
            self._connection_to_cycle[key] = count
            self._connections[key].send_message(
              Messages.tick(0, self._game_number, [[Messages.player_number(count)]])
            )
            self._connections_message_to_receive[key] = [0]
            self._light_cycles[count] = Light_cycle(None, count, True)
            self._light_cycles[count].set_location(Settings.CYCLE_LOCATIONS[count])
            self._light_cycles[count].set_direction(Settings.CYCLE_DIRECTIONS[count])
            count += 1
        
        for i in range(count, Settings.MATCHMAKER_MAXIMUM_PLAYERS):
            self._light_cycles[i] = Light_cycle(None, i, True)
            self._light_cycles[i].set_location(Settings.CYCLE_LOCATIONS[i])
            self._light_cycles[i].set_direction(Settings.CYCLE_DIRECTIONS[i])
            self._light_cycles[i].set_trail_on(None)
            self._light_cycles_ai[i] = Ai(self._light_cycles, i)
        
        for cycle in self._light_cycles.itervalues():
            cycle.move_tick(0)
            
        self._send_messages_for_tick()
        
        self._tick_number += 1
        
    
    def get_game_over(self):
        return self._game_over
    
    
    def get_game_number(self):
        return self._game_number
    
    
    def end_game(self):
        if self._game_over:
            return
        self._game_over = True
        for key in self._connections:
            won = False
            if len(self._light_cycles) == 1:
                if self._connection_to_cycle[key] in self._light_cycles:
                    won = True
            # send extra messages because of client delay
            self._connections[key].send_message(
              Messages.tick(self._tick_number, self._game_number, [[Messages.game_over(won)]])
            )
            self._connections[key].send_message(
              Messages.tick(self._tick_number + 1, self._game_number, [[Messages.game_over(won)]])
            )
            self._connections[key].send_message(
              Messages.tick(self._tick_number + 2, self._game_number, [[Messages.game_over(won)]])
            )
            self._connections[key].set_game(None)
        logging.debug('end_game, _game_number: ' + str(self._game_number) + ' _tick_number: ' + str(self._tick_number))
        
        for key in self._connections:
            logging.debug('end_game, self._connections_message_to_receive[key]: ' + str(self._connections_message_to_receive[key]))


    def get_connections(self):
        return self._connections


    def message(self, message, connection_number):
        message_decoded = json.loads(message)
        if message_decoded['tick_number'] < self._tick_number - 8:
            return
        if message_decoded['tick_number'] > self._tick_number:
            return
        message_decoded['connection_number'] = connection_number
        self._messages.append(message_decoded)

    
    def tick(self):
        if self._waiting_for_startup:
            self._startup_tick()
            return
        
        elapsed_time = time.time() - self._last_tick_time
        
        self._tick_ai()
        
        self._process_messages()
        
        if self._tick_number > 10:
            self._cycle_move_tick(elapsed_time)
            self._check_for_collisions()
        
        self._send_messages_for_tick()
        
        self._cleanup_dead_cycles()
        
        self._check_message_history()
        
        self._tick_number += 1
        self._last_tick_time = time.time()
    
    
    def _startup_tick(self):
        self._process_messages()
        self._check_message_history()
        if self._message_history_tick > 1:
            self._waiting_for_startup = False
            return
        self._waiting_for_startup_ticks += 1
        print 'waiting for client startup'
        if self._waiting_for_startup_ticks > 5.0 / Settings.TICK:
            for key in self._connections:
                if self._message_history_tick in self._connections_message_to_receive[key]:
                    self.drop_connection(key)
            self._cleanup_dropped_connections()
        
        
    def _tick_ai(self):
        if not self._light_cycles_ai:
            return
        
        for key in self._light_cycles_ai:
            command = self._light_cycles_ai[key].tick()
            if command == 'left':
                self._light_cycles[key].turn_left()
                continue
            if command == 'double_left':
                self._light_cycles[key].turn_left()
                self._light_cycles[key].turn_left()
                continue
            if command == 'right':
                self._light_cycles[key].turn_right()
                continue
            if command == 'double_right':
                self._light_cycles[key].turn_right()
                self._light_cycles[key].turn_right()
                continue
    
    
    def _process_messages(self):
        while self._messages:
            message = self._messages.pop()
            connection_number = message['connection_number']
            key = self._connection_to_cycle.get(connection_number, None)
            if key is None:
                continue
            if key not in self._light_cycles:
                continue
            if message['message_type'] == Settings.MESSAGE_TYPE_TICK:
                if message['game_number'] != self._game_number:
                    continue
                message_list = message['messages']
                for message in message_list:
                    if message['message_type'] == Settings.MESSAGE_TYPE_INPUT:
                        if message['input_type'] == 'up':
                            self._light_cycles[key].raise_speed()
                            continue
                        if message['input_type'] == 'down':
                            self._light_cycles[key].lower_speed()
                            continue
                        if message['input_type'] == 'left':
                            self._light_cycles[key].turn_left()
                            continue
                        if message['input_type'] == 'right':
                            self._light_cycles[key].turn_right()
                            continue
                        if message['input_type'] == 'space':
                            self._light_cycles[key].toggle_trail()
                            continue
                        if message['input_type'] == 'quit':
                            self.drop_connection(connection_number)
                            continue
                        print 'unhandled message in _process_messages: ' + str(message)
            if message['message_type'] == Settings.MESSAGE_TYPE_TICK_RECEIVED:
                if message['tick_number'] != 0:
                    if message['game_number'] != self._game_number:
                        continue
                try:
                    self._connections_message_to_receive[connection_number].remove(message['tick_number'])
                except ValueError:
                    pass

    
    def _cycle_move_tick(self, elapsed_time):
            for cycle in self._light_cycles.itervalues():
                cycle.move_tick(elapsed_time)
    
    
    def _check_for_collisions(self):
        for key in self._light_cycles:
            if self._light_cycles[key].is_alive():
                for cycle in self._light_cycles.itervalues():
                    self._light_cycles[key].collision(cycle)
            else:
                self._dead_cycles.append(key)
        
    
    def _send_messages_for_tick(self):
        messages = []
        for cycle in self._light_cycles.itervalues():
            cycle_message = cycle.get_and_delete_messages()
            if cycle_message != []:
                messages.append(cycle_message)
            cycle_message = cycle.trail_get_and_delete_messages()
            if cycle_message != []:
                messages.append(cycle_message)
        
        self._message_history[self._tick_number] = Messages.tick(self._tick_number, self._game_number, messages)
        
        for key in self._connections:
            self._connections[key].send_message(self._message_history[self._tick_number])
            self._connections_message_to_receive[key].append(self._tick_number)
    
    
    def _cleanup_dead_cycles(self):
        while self._dead_cycles:
            key = self._dead_cycles.pop()
            if key in self._light_cycles:
                del self._light_cycles[key]
                if key in self._light_cycles_ai:
                    del self._light_cycles_ai[key]
        
        if len(self._light_cycles) < 2:
            self.end_game()


    def _check_message_history(self):
        while self._message_history_tick < self._tick_number:
            found = False
            for key in self._connections:
                if self._message_history_tick in self._connections_message_to_receive[key]:
                    if self._message_history_tick + 2 < self._tick_number:
                        self._connections[key].send_message(self._message_history[self._message_history_tick])
                        logging.debug('resent tick, _game_number: ' + str(self._game_number) + ' _message_history_tick: ' + str(self._message_history_tick))
                    if self._message_history_tick < self._tick_number - 5:
                        found = True
                    else:
                        self._connections_message_to_receive[key].remove(self._message_history_tick)
            if found:
                break
            else:
                self._message_history_tick += 1
        
        for i in range(self._message_history_tick + 1, self._tick_number - 3):
            for key in self._connections:
                if i in self._connections_message_to_receive[key]:
                    self._connections[key].send_message(self._message_history[i])
                    logging.debug('resent tick, _game_number: ' + str(self._game_number) + ' i: ' + str(i))

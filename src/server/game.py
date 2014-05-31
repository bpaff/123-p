
import time
import json
import logging

from common.ai import Ai
from common.settings import Settings
from common.messages import Messages
from common.light_cycle import Light_cycle


class Game():
    
    def __init__(self, games, game_number):
        self._games = games
        self._game_number = game_number
        self._connections = {}
        self._connections_ok_to_start_game = {}
        self._connection_to_drop = []
        self._connection_to_cycle = {}
        self._light_cycles = {}
        self._light_cycles_ai = {}
        self._dead_cycles = []
        self._game_over = False
        self._tick_number = 1
        self._last_tick_time = None
        self._messages = []
        self._message_history = {}
        self._message_resend_count = {}
        self._waiting_for_startup = True
        self._waiting_for_startup_ticks = 0
    
    
    def add_connection(self, connection):
        connection_number = connection.get_connection_number()
        self._connections[connection_number] = connection
        self._connections_ok_to_start_game[connection_number] = False
        connection.set_game(self)
    
    
    def drop_connection(self, connection_number):
        if connection_number in self._connections:
            if connection_number not in self._connection_to_drop:
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
        logging.debug('start_game return, _game_number: ' + str(self._game_number))
    
    
    def _cleanup_dropped_connections(self):
        while self._connection_to_drop:
            connection_number = self._connection_to_drop.pop()
            logging.debug('_cleanup_dropped_connections, connection_number: ' + str(connection_number))
            if connection_number in self._connections:
                self._connections[connection_number].set_game(None)
                self._connections[connection_number].on_close()
                self._connections[connection_number].close()
                del self._connections[connection_number]
                del self._connections_ok_to_start_game[connection_number]
                del self._message_resend_count[connection_number]
            if not self._light_cycles:
                break
            cycle_number = self._connection_to_cycle.get(connection_number, None)
            if cycle_number is None:
                break
            del self._connection_to_cycle[connection_number]
            if cycle_number not in self._light_cycles:
                break
            self._light_cycles_ai[cycle_number] = Ai(True, self._light_cycles, cycle_number)
        
        if not self._connections:
            self.end_game()
        
    
    def _create_light_cycles(self):
        count = 0
        for key in self._connections:
            self._connection_to_cycle[key] = count
            self._connections[key].send_message(
              Messages.tick(0, self._game_number, [Messages.player_number(count)])
            )
            self._message_resend_count[key] = 0
            self._light_cycles[count] = Light_cycle(None, count, True)
            self._light_cycles[count].set_location(Settings.CYCLE_LOCATIONS[count])
            self._light_cycles[count].set_direction(Settings.CYCLE_DIRECTIONS[count])
            count += 1
        
        for i in range(count, Settings.MATCHMAKER_MAXIMUM_PLAYERS):
            self._light_cycles[i] = Light_cycle(None, i, True)
            self._light_cycles[i].set_location(Settings.CYCLE_LOCATIONS[i])
            self._light_cycles[i].set_direction(Settings.CYCLE_DIRECTIONS[i])
            self._light_cycles[i].set_trail_on(None)
            self._light_cycles_ai[i] = Ai(True, self._light_cycles, i)
        
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
              Messages.tick(self._tick_number, self._game_number, [Messages.game_over(won)])
            )
            self._connections[key].send_message(
              Messages.tick(self._tick_number + 1, self._game_number, [Messages.game_over(won)])
            )
            self._connections[key].send_message(
              Messages.tick(self._tick_number + 2, self._game_number, [Messages.game_over(won)])
            )
            self._connections[key].set_game(None)
        logging.debug('end_game, _game_number: ' + str(self._game_number) + ' _tick_number: ' + str(self._tick_number))


    def message(self, message, connection_number):
        message_decoded = json.loads(message)
        if int(message_decoded['game']) != self._game_number:
            logging.debug('message, wrong game number, _game_number: ' + str(self._game_number) + ' message_decoded: ' + str(message_decoded))
            return
        if int(message_decoded['tick']) > self._tick_number:
            logging.debug('message, tick number to high, _tick_number: ' + str(self._tick_number) + ' message_decoded: ' + str(message_decoded))
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
        
        self._cleanup_dropped_connections()
        
        self._cleanup_dead_cycles()
        
        self._tick_number += 1
        self._last_tick_time = time.time()
    
    
    def _startup_tick(self):
        self._process_messages()
        
        self._waiting_for_startup = False
        for key in self._connections:
            if not self._connections_ok_to_start_game[key]:
                self._waiting_for_startup = True
                break
        
        self._waiting_for_startup_ticks += 1
        if self._waiting_for_startup_ticks > 3.0 / Settings.TICK:
            for key in self._connections:
                if not self._connections_ok_to_start_game[key]:
                    self.drop_connection(key)
            self._cleanup_dropped_connections()
        
        
    def _tick_ai(self):
        if not self._light_cycles_ai:
            return
        
        for key in self._light_cycles_ai:
            command = self._light_cycles_ai[key].tick(self._tick_number, 10)
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
            key = self._connection_to_cycle.get(message['connection_number'], None)
            if key is None:
                continue
            
            if message['type'] == Settings.MESSAGE_TYPE_QUIT_GAME:
                self.drop_connection(message['connection_number'])
                continue
            
            if message['type'] == Settings.MESSAGE_TYPE_START_GAME:
                self._connections_ok_to_start_game[message['connection_number']] = True
            
            if message['type'] == Settings.MESSAGE_TYPE_RESEND_TICK:
                self._connections[message['connection_number']].send_message(self._message_history[int(message['tick'])])
                self._message_resend_count[message['connection_number']] += 1
                logging.debug('resent tick, connection_number: ' + str(message['connection_number']) + ' _game_number: ' + str(self._game_number) + ' tick: ' + str(int(message['tick'])))
            
            if key not in self._light_cycles:
                continue
            
            if message['type'] == Settings.MESSAGE_TYPE_TICK:
                message_list = message['messages']
                for message in message_list:
                    if message['type'] == Settings.MESSAGE_TYPE_INPUT:
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
                        logging.debug('_process_messages, unhandled message: ' + str(message))

    
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
            while True:
                try:
                    message = cycle.get_messages().pop()
                except IndexError:
                    break
                messages.append(message)
            while True:
                try:
                    message = cycle.trail_get_messages().pop()
                except IndexError:
                    break
                messages.append(message)
        
        self._message_history[self._tick_number] = Messages.tick(self._tick_number, self._game_number, messages)
        
        for key in self._connections:
            self._connections[key].send_message(self._message_history[self._tick_number])
    
    
    def _cleanup_dead_cycles(self):
        while self._dead_cycles:
            key = self._dead_cycles.pop()
            if key in self._light_cycles:
                del self._light_cycles[key]
                if key in self._light_cycles_ai:
                    del self._light_cycles_ai[key]
        
        if len(self._light_cycles) < 2:
            self.end_game()
            


import time
import logging
import json

import pygame


from common.settings import Settings
from user_input import User_input
from common.messages import Messages
from common.colors import Colors
from common.light_cycle import Light_cycle


class Game():
    
    def __init__(self):
        logging.basicConfig(filename='client.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
        pygame.init()
        self._surface = pygame.display.set_mode(Settings.SCREEN_DIMENSIONS)
        pygame.display.set_caption(Settings.CAPTION)
        pygame.mouse.set_visible(False)
        self._font_helvettica = pygame.font.SysFont('helvettica', 24)
        self._connection_host = None
        self._connection = None
        self._user_input = User_input(self)
        self._keep_running = True
        self._last_tick_time = None
        self._show_instructions = True
        self._text = None
        # per game variables
        self._light_cycles = {}
        self._messages_on_tick = {}
        self._game_over = False
        self._game_number = None
        self._player_number = None
        self._tick_number = 0
        self._skipped_ticks = 0
        self._no_message_ticks = 0
        self._wins = 0
        self._loses = 0    


    def set_text(self, text):
        self._text = text
        self._update_display()


    def get_connection_address(self):
        text_start = 'Please enter server to connect to: '
        text_back = Settings.CLIENT_HOST
        self.set_text(text_start + text_back)
        while True:
            data = self._user_input.get_text_input()
            if data is None:
                continue
            if data == 'quit':
                return
            if data == 'return':
                if text_back != '':
                    break
                continue
            if data == 'backspace':
                text_back = text_back[:-1]
            else:
                if data.isalpha() or data.isdigit() or data == '.':
                    text_back += data
            self.set_text(text_start + text_back)
        self._connection_host = text_back
        
    
    def get_connection_host(self):    
        return self._connection_host


    def set_connection(self, connection):
        self._connection = connection
    
    
    def get_tick_number(self):
        return self._tick_number
    
        
    def message(self, message):
        message_decoded = json.loads(message)
        tick_number = int(message_decoded['tick_number'])
        if tick_number < self._tick_number:
            return
        if tick_number not in self._messages_on_tick:
            self._messages_on_tick[tick_number] = []
        self._messages_on_tick[tick_number].append(message_decoded)
        self._connection.send_message(Messages.tick_received(tick_number, self._game_number))
    
    
    def run(self):
        while self._keep_running:
            self._phase_wait_for_server()
            self._phase_load_cycles()
            self._phase_play_game()

    
    def stop(self):
        self._keep_running = False


    def _phase_wait_for_server(self):
        self.set_text('Searching for game...')
        
        self._light_cycles = {}
        self._messages_on_tick = {}
        self._game_over = False
        self._game_number = None
        self._player_number = None
        self._tick_number = 0
        self._skipped_ticks = 0
        self._no_message_ticks = 0
        
        while self._keep_running:
            self._user_input.get_input()
            if 0 in self._messages_on_tick:
                self._process_messages()
                break
            self._connection.poll(Settings.TICK / 2.0, 2)
    
    
    def _phase_load_cycles(self):
        logging.debug('_phase_load_cycles, _game_number: ' + str(self._game_number) + ' _player_number: ' + str(self._player_number))
        
        while self._keep_running:
            self._user_input.get_input()
            if 1 in self._messages_on_tick:
                self._process_messages()
                break
            self._connection.poll(Settings.TICK / 2.0, 2)
        
        for key in self._light_cycles:
            if key == self._player_number:
                continue
            self._light_cycles[key].set_color(Colors.CYCLE_COLORS[key])
            self._light_cycles[key].set_trail_color(Colors.CYCLE_COLORS[key])
        
        self._text = None
        self._show_instructions = False
        self._update_display()
        
        self._user_input.get_input()
        self._user_input.get_and_delete_messages()
    
    
    def _phase_play_game(self):
        logging.debug('_phase_play_game, _game_number: ' + str(self._game_number) + ' _player_number: ' + str(self._player_number))
        
        while self._keep_running:
            start_time = time.time()
            
            self._user_input.get_input()
            messages = self._user_input.get_and_delete_messages()
            if messages != []:
                self._connection.send_message(Messages.tick(self._tick_number, self._game_number, messages))
            
            if self._tick_number + 2 in self._messages_on_tick:
                self._process_messages()
                self._update_display()
                self._skipped_ticks = 0
                self._no_message_ticks = 0
            else:
                if self._tick_number + 1 in self._messages_on_tick or self._tick_number in self._messages_on_tick:
                    if self._skipped_ticks > 1.0 / Settings.TICK:
                        logging.debug('skipped tick , _game_number: ' + str(self._game_number) + ' _player_number: ' + str(self._player_number) + ' _tick_number: ' + str(self._tick_number))
                        self._skipped_ticks = 0
                        self._no_message_ticks = 0
                        self._tick_number += 1
                    self._skipped_ticks += 1
                else:
                    if self._no_message_ticks > 5.0 / Settings.TICK:
                        self._game_over = True
                        logging.debug('no message tick , _game_number: ' + str(self._game_number) + ' _player_number: ' + str(self._player_number) + ' _tick_number: ' + str(self._tick_number))
                    self._no_message_ticks += 1
            
            if self._tick_number + 2 in self._messages_on_tick:
                sleep_time = (Settings.TICK / 2.0) - (time.time() - start_time)
                if sleep_time > 0.001:
                    time.sleep(sleep_time)
            else:
                self._connection.poll(Settings.TICK / 5.0, 5)
            
            if self._game_over:
                break
        
        logging.debug('_phase_play_game, _game_number: ' + str(self._game_number) + ' _player_number: ' + str(self._player_number) + ' _tick_number: ' + str(self._tick_number))


    def _process_messages(self):
        # process game messages
        while self._messages_on_tick[self._tick_number]:
            message = self._messages_on_tick[self._tick_number].pop()
            if message['message_type'] == Settings.MESSAGE_TYPE_TICK:
                if self._game_number is None:
                    self._game_number = message['game_number']
                if message['game_number'] != self._game_number:
                    continue
                message_list = message['messages']
                for messages in message_list:
                    for message in messages:
                        if message['message_type'] == Settings.MESSAGE_TYPE_CYCLE_POSITION:
                            key = int(message['cycle_number'])
                            if self._tick_number == 1:
                                self._light_cycles[key] = Light_cycle(self._surface, key, False)
                            if key in self._light_cycles:
                                self._light_cycles[key].set_cycle_position(message['cycle_position'])
                            continue
                        if message['message_type'] == Settings.MESSAGE_TYPE_CYCLE_ALIVE:
                            key = int(message['cycle_number'])
                            if message['is_alive']:
                                continue
                            if key in self._light_cycles:
                                del self._light_cycles[key]
                            continue
                        if message['message_type'] == Settings.MESSAGE_TYPE_TRAIL_ON:
                            key = int(message['cycle_number'])
                            if key in self._light_cycles:
                                if message['trail_on']:
                                    self._light_cycles[key].set_trail_on(message['location'])
                                else:
                                    self._light_cycles[key].set_trail_off(message['location'])
                            continue
                        if message['message_type'] == Settings.MESSAGE_TYPE_TRAIL_TURN:
                            key = int(message['cycle_number'])
                            if key in self._light_cycles:
                                self._light_cycles[key].set_trail_turn(message['location'])  
                            continue
                        if message['message_type'] == Settings.MESSAGE_TYPE_GAME_OVER:
                            self._game_over = True
                            if message['won']:
                                self._wins += 1
                            else:
                                self._loses += 1
                            return
                        if message['message_type'] == Settings.MESSAGE_TYPE_PLAYER:
                            self._player_number = message['player']
                            continue
                        print 'unhandled message in _process_messages: ' + str(message)
        
        del self._messages_on_tick[self._tick_number]
        self._tick_number += 1


    def _update_display(self):
        self._surface.fill(Colors.BLACK)
        
        pygame.draw.line(
          self._surface,
          Colors.SILVER,
          (0, Settings.BOARD_DIMENSIONS[1]),
          (Settings.BOARD_DIMENSIONS[0], Settings.BOARD_DIMENSIONS[1]),
          2
        )
        
        if self._show_instructions:
            height = 15
            for line in Settings.INSTRUCTIONS:
                line = self._font_helvettica.render(line, 1, Colors.WHITE)
                self._surface.blit(line, (15, height))
                height += 25
        else:
            line = self._font_helvettica.render('Wins     ' + str(self._wins), 1, Colors.WHITE)
            self._surface.blit(line, (Settings.BOARD_DIMENSIONS[0] - 100, Settings.BOARD_DIMENSIONS[1] + 25))
            line = self._font_helvettica.render('Loses   ' + str(self._loses), 1, Colors.WHITE)
            self._surface.blit(line, (Settings.BOARD_DIMENSIONS[0] - 100, Settings.BOARD_DIMENSIONS[1] + 50))
            
        if self._text is not None:
            text = self._font_helvettica.render(self._text, 1, Colors.WHITE)
            self._surface.blit(text, (15, Settings.BOARD_DIMENSIONS[1] + 15))
            
        for cycle in self._light_cycles.itervalues():
            cycle.update_cycle_surface()
            cycle.update_trail_surface()
        
        pygame.display.update()

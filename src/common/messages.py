
import json


from common.settings import Settings


class Messages():
    
    
    @staticmethod
    def tick(tick_number, game_number, messages):
        return json.dumps({
          'type':Settings.MESSAGE_TYPE_TICK,
          'tick':tick_number,
          'game':game_number,
          'messages':messages
        })
    
    
    @staticmethod
    def player_input(input_type):
        return {
          'type':Settings.MESSAGE_TYPE_INPUT,
          'input_type':input_type
        }
        
    
    @staticmethod
    def player_number(player_number):
        return {
          'type':Settings.MESSAGE_TYPE_PLAYER,
          'player':player_number
        }
    
    
    @staticmethod
    def cycle_position(cycle_number, cycle_position):
        return {
          'type':Settings.MESSAGE_TYPE_CYCLE_POSITION,
          'cycle_number':cycle_number,
          'cycle_position':cycle_position
        }


    @staticmethod
    def cycle_alive(cycle_number, is_alive):
        return {
          'type':Settings.MESSAGE_TYPE_CYCLE_ALIVE,
          'cycle_number':cycle_number,
          'is_alive':is_alive
        }
    
    
    @staticmethod
    def trail_on(cycle_number, trail_on, location):
        return {
          'type':Settings.MESSAGE_TYPE_TRAIL_ON,
          'cycle_number':cycle_number,
          'trail_on':trail_on,
          'location':location
        }
    
    
    @staticmethod
    def trail_turn(cycle_number, location):
        return {
          'type':Settings.MESSAGE_TYPE_TRAIL_TURN,
          'cycle_number':cycle_number,
          'location':location
        }

    
    @staticmethod
    def game_over(won):
        return {
          'type':Settings.MESSAGE_TYPE_GAME_OVER,
          'won':won
        }


    @staticmethod
    def start_game(tick_number, game_number):
        return json.dumps({
          'type':Settings.MESSAGE_TYPE_START_GAME,
          'tick':tick_number,
          'game':game_number
        })
    
    
    @staticmethod
    def quit_game(tick_number, game_number):
        return json.dumps({
          'type':Settings.MESSAGE_TYPE_QUIT_GAME,
          'tick':tick_number,
          'game':game_number
        })
        
    @staticmethod
    def resend_tick(tick_number, game_number):
        return json.dumps({
          'type':Settings.MESSAGE_TYPE_RESEND_TICK,
          'tick':tick_number,
          'game':game_number
        })

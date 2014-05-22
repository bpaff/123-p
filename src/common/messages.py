
import json


from common.settings import Settings


class Messages():
    
    
    @staticmethod
    def tick(tick_number, game_number, messages):
        return json.dumps({
          'message_type':Settings.MESSAGE_TYPE_TICK,
          'tick_number':tick_number,
          'game_number':game_number,
          'messages':messages
        })
    
    
    @staticmethod
    def player_input(input_type):
        return {
          'message_type':Settings.MESSAGE_TYPE_INPUT,
          'input_type':input_type
        }
        
    
    @staticmethod
    def player_number(player_number):
        return {
          'message_type':Settings.MESSAGE_TYPE_PLAYER,
          'player':player_number
        }
    
    
    @staticmethod
    def cycle_position(cycle_number, cycle_position):
        return {
          'message_type':Settings.MESSAGE_TYPE_CYCLE_POSITION,
          'cycle_number':cycle_number,
          'cycle_position':cycle_position
        }


    @staticmethod
    def cycle_alive(cycle_number, is_alive):
        return {
          'message_type':Settings.MESSAGE_TYPE_CYCLE_ALIVE,
          'cycle_number':cycle_number,
          'is_alive':is_alive
        }
    
    
    @staticmethod
    def trail_on(cycle_number, trail_on, location):
        return {
          'message_type':Settings.MESSAGE_TYPE_TRAIL_ON,
          'cycle_number':cycle_number,
          'trail_on':trail_on,
          'location':location
        }
    
    
    @staticmethod
    def trail_turn(cycle_number, location):
        return {
          'message_type':Settings.MESSAGE_TYPE_TRAIL_TURN,
          'cycle_number':cycle_number,
          'location':location
        }

    
    @staticmethod
    def game_over(won):
        return {
          'message_type':Settings.MESSAGE_TYPE_GAME_OVER,
          'won':won
        }


    @staticmethod
    def tick_received(tick_number, game_number):
        return json.dumps({
          'message_type':Settings.MESSAGE_TYPE_TICK_RECEIVED,
          'tick_number':tick_number,
          'game_number':game_number
        })
    
    
    @staticmethod
    def quit_game(tick_number, game_number):
        return json.dumps({
          'message_type':Settings.MESSAGE_TYPE_QUIT_GAME,
          'tick_number':tick_number,
          'game_number':game_number
        })

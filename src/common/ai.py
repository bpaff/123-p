
import random

from common.settings import Settings
from common.rotation import Rotation
from common.transform import Transform


class Ai():
    
    def __init__(self, is_server, light_cycles, cycle_number):
        self._is_server = is_server
        self._light_cycles = light_cycles
        self._cycle_number = cycle_number
        self._ai_wait_seconds_min = 0.6
        self._ai_wait_seconds_max = 6.0
        self._ai_wait_ticks = 10
        self._ai_tick = 0
        self._location = [0, 0]
        self._direction = 0
        self._speed = 0
        self._command_list = {}
        self._tick_number = 0
        if self._is_server:
            self._ai_ticks_ahead = Settings.SERVER_AI_LOOK_AHEAD_TICKS
        else:
            self._ai_ticks_ahead = Settings.CLIENT_AI_LOOK_AHEAD_TICKS 
        
    
    
    def tick(self, tick_number, ai_number_of_commands_received):
        self._tick_number = tick_number
        
        cycle_position = self._light_cycles[self._cycle_number].get_cycle_position()
        self._location = cycle_position['location']
        self._direction = cycle_position['direction']
        self._speed = self._light_cycles[self._cycle_number].get_speed()
        
        
        if self._is_server:
            if self._command_list:
                self._command_list = {}
        else:
            for _ in range(0, ai_number_of_commands_received):
                if not self._command_list:
                    break
                key = min(self._command_list)
                del self._command_list[key]
        
        
        good_list = {}
        
        good_list['current'] = self._get_tick_number_good_till();

        self._direction -= 45
        if self._direction < 0:
            self._direction = 315
        good_list['left'] = self._get_tick_number_good_till();
        self._direction -= 45
        if self._direction < 0:
            self._direction = 315
        good_list['double_left'] = self._get_tick_number_good_till();
        
        self._direction = cycle_position['direction']
        self._direction += 45
        if self._direction > 315:
            self._direction = 0
        good_list['right'] = self._get_tick_number_good_till();
        self._direction += 45
        if self._direction > 315:
            self._direction = 0
        good_list['double_right'] = self._get_tick_number_good_till();
        
        max_tick = max(good_list.itervalues())

        if good_list['current'] == max_tick:
            self._ai_tick += 1
             
            if self._ai_tick < self._ai_wait_ticks:
                return None
             
            self._ai_tick = 0
            self._ai_wait_ticks = random.randint(int(self._ai_wait_seconds_min / Settings.TICK), int(self._ai_wait_seconds_max / Settings.TICK))
            
            if good_list['left'] == good_list['right']:
                self._command_list[self._tick_number + 2] = self._random_left_or_right()
                return self._command_list[self._tick_number + 2]
            if good_list['left'] > good_list['right']:
                self._command_list[self._tick_number + 2] = 'left'
                return 'left'
            else:
                self._command_list[self._tick_number + 2] = 'right'
                return 'right'
        
        self._ai_tick = 0
        
        if good_list['left'] == max_tick:
            if good_list['left'] == good_list['right']:
                self._command_list[self._tick_number + 2] = self._random_left_or_right()
                return self._command_list[self._tick_number + 2]
        if good_list['left'] == max_tick:
            self._command_list[self._tick_number + 2] = 'left'
            return 'left'
        if good_list['right'] == max_tick:
            self._command_list[self._tick_number + 2] = 'right'
            return 'right'
        
        if good_list['double_left'] == max_tick:
            self._command_list[self._tick_number + 2] = 'double_left'
            return 'double_left'
        if good_list['double_right'] == max_tick:
            self._command_list[self._tick_number + 2] = 'double_right'
            return 'double_right'
        
        return None


    def _get_tick_number_good_till(self):
        direction = self._direction
        if self._command_list:
            for command in self._command_list.itervalues():
                if command == 'left':
                    direction -= 45
                    if direction < 0:
                        direction = 315
                elif command == 'right':
                    direction += 45
                    if direction > 315:
                        direction = 0
                elif command == 'double_left':
                    direction -= 45
                    if direction < 0:
                        direction = 315
                    direction -= 45
                    if direction < 0:
                        direction = 315
                elif command == 'double_right':
                    direction += 45
                    if direction > 315:
                        direction = 0
                    direction += 45
                    if direction > 315:
                        direction = 0
        
        for i in range(1, self._ai_ticks_ahead + 1):
            point = Transform.make_point(self._location, direction, self._speed, i * Settings.TICK)
            if self._going_outside_board(point):
                return i - 1
            lines = self._get_lines_rotated_location(direction, self._location, i * Settings.TICK)
            if self._going_to_hit_wall(lines):
                return i - 1
        return self._ai_ticks_ahead
    
    

    def _going_outside_board(self, point):
        if point[0] < 0 or point[0] > Settings.BOARD_DIMENSIONS[0]:
            return True
        if point[1] < 0 or point[1] > Settings.BOARD_DIMENSIONS[1]:
            return True
        return False
    
    
    def _going_to_hit_wall(self, lines):
        for light_cycle in self._light_cycles.itervalues():
            if light_cycle.collision_lines(lines, self._cycle_number):
                return True
        return False
    
    
    def _random_left_or_right(self):
        if random.randint(0, 9) > 4: 
            return 'left'
        else:
            return 'right'
    
    
    def _get_lines_rotated_location(self, direction, location, time_passed):
        lines = (
            ((Settings.LIGHT_CYCLE_SIZE[0] / 2.0, 0),
            (Settings.LIGHT_CYCLE_SIZE[0] / 2.0, -Settings.LIGHT_CYCLE_SIZE[1] - (self._speed * time_passed))),
            ((-Settings.LIGHT_CYCLE_SIZE[0] / 2.0, 0),
            (-Settings.LIGHT_CYCLE_SIZE[0] / 2.0, -Settings.LIGHT_CYCLE_SIZE[1] - (self._speed * time_passed)))
        )
        lines = Rotation.rotate_lines(lines, direction, (0, 0), (0, 0))
        return Transform.move_lines(lines, location)


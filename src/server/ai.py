
import random

from common.settings import Settings
from common.rotation import Rotation
from common.transform import Transform


class Ai():
    
    def __init__(self, light_cycles, cycle_number):
        self._light_cycles = light_cycles
        self._cycle_number = cycle_number
        self._ai_wait_seconds_min = 0.6
        self._ai_wait_seconds_max = 5.0
        self._ai_wait_ticks = 10
        self._ai_tick = 0
    
    
    def tick(self):
        cycle_position = self._light_cycles[self._cycle_number].get_cycle_position()
        location = cycle_position['location']
        direction = cycle_position['direction']
        speed = self._light_cycles[self._cycle_number].get_speed()
        
        good_for_current = True
        good_for_left = True
        good_for_double_left = True
        good_for_right = True
        good_for_double_right = True
        
        
        point = Transform.make_point(location, direction, speed, Settings.TICK * 4)
        if self._going_outside_board(point):
            good_for_current = False
        lines = self._get_middle_lines_rotated_location(direction, point)
        if self._going_to_hit_wall(lines):
            good_for_current = False

        direction -= 45
        if direction < 0:
            direction = 315
        point = Transform.make_point(location, direction, speed, Settings.TICK * 3)
        if self._going_outside_board(point):
            good_for_left = False
        lines = self._get_middle_lines_rotated_location(direction, point)
        if self._going_to_hit_wall(lines):
            good_for_left = False
            
        direction -= 45
        if direction < 0:
            direction = 315
        point = Transform.make_point(location, direction, speed, Settings.TICK * 2)
        if self._going_outside_board(point):
            good_for_double_left = False
        lines = self._get_middle_lines_rotated_location(direction, point)
        if self._going_to_hit_wall(lines):
            good_for_double_left = False

        direction = cycle_position['direction']
        direction += 45
        if direction > 315:
            direction = 0
        point = Transform.make_point(location, direction, speed, Settings.TICK * 3)
        if self._going_outside_board(point):
            good_for_right = False
        lines = self._get_middle_lines_rotated_location(direction, point)
        if self._going_to_hit_wall(lines):
            good_for_right = False
        
        direction += 45
        if direction > 315:
            direction = 0
        point = Transform.make_point(location, direction, speed, Settings.TICK * 2)
        if self._going_outside_board(point):
            good_for_double_right = False
        lines = self._get_middle_lines_rotated_location(direction, point)
        if self._going_to_hit_wall(lines):
            good_for_double_right = False
        

        if good_for_current:
            self._ai_tick += 1
             
            if self._ai_tick < self._ai_wait_ticks:
                return None
             
            self._ai_tick = 0
            self._ai_wait_ticks = random.randint(int(self._ai_wait_seconds_min / Settings.TICK), int(self._ai_wait_seconds_max / Settings.TICK))
            
            if good_for_left and good_for_right:
                return self._random_left_or_right()
            if good_for_left:
                return 'left'
            if good_for_right:
                return 'right'
            return None
        
        self._ai_tick = 0
        
        if good_for_left and good_for_right:
            return self._random_left_or_right()
        if good_for_left:
            return 'left'
        if good_for_right:
            return 'right'
        
        if good_for_double_left and good_for_double_right:
            return self._random_left_or_right()
        if good_for_double_left:
            return 'double_left'
        if good_for_double_right:
            return 'double_right'
        
        return None


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
    
    
    def _get_middle_lines_rotated_location(self, direction, location):
        middle_lines_rotated = Rotation.rotate_lines(Settings.MIDDLE_LINES, direction, (0, 0), (0, 0))
        return Transform.move_lines(middle_lines_rotated, location)


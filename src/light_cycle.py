
import time
import math
import pygame
from random import randint

from settings import Settings
from colors import Colors
from cycle_trail import Cycle_trail
from rotation import Rotation
from transform import Transform
from collision import Collision


class Light_cycle():
    
    DIRECTION_UP = 0
    DIRECTION_UP_RIGHT = 45
    DIRECTION_RIGHT = 90
    DIRECTION_DOWN_RIGHT = 135
    DIRECTION_DOWN = 180
    DIRECTION_DOWN_LEFT = 225
    DIRECTION_LEFT = 270
    DIRECTION_UP_LEFT = 315
    
    def __init__(self, surface):
        self._surface = surface
        self._pixel_per_time_passed = 1.0 / 200.0
        self._speed_adjustment = 1.0
        self._color = Colors.STEELBLUE
        self._size = Settings.LIGHT_CYCLE_SIZE
        self._max_size = max(self._size[0], self._size[1])
        self._direction = self.DIRECTION_DOWN_RIGHT
        self._alive = True
        self._location = [100, 100]
        self._speed = 10.0
        radians = math.radians(self._direction - 135)
        self._cos = math.cos(radians)
        self._sin = math.sin(radians)
        self._update_cycle_rotation()
        self._update_cycle_surface()
        self._trail = Cycle_trail(surface)
        self._is_ai = False
        self._ai_tick = 0
        self._ai_wait = 50
        
    def _update_cycle_rotation(self):
        self._back_wheel_points_rotated = Rotation.rotate_points(Settings.BACK_WHEEL_POINTS, self._direction, (0, 0), (0, 0))
        self._middle_points_rotated = Rotation.rotate_points(Settings.MIDDLE_POINTS, self._direction, (0, 0), (0, 0))
        self._front_wheel_points_rotated = Rotation.rotate_points(Settings.FRONT_WHEEL_POINTS, self._direction, (0, 0), (0, 0))
        self._middle_lines_rotated = Rotation.rotate_lines(Settings.MIDDLE_LINES, self._direction, (0, 0), (0, 0))
        self._driver_window_points_rotated = Rotation.rotate_points(Settings.DRIVER_WINDOW_POINTS, self._direction, (0, 0), (0, 0))
        
        self._middle_lines_rotated_location = Transform.move_lines(self._middle_lines_rotated, self._location) 
    
    def _update_cycle_surface(self):
        pygame.draw.polygon(self._surface, self._color,
                            Transform.move_points(self._back_wheel_points_rotated, self._location))
        pygame.draw.polygon(self._surface, self._color,
                            Transform.move_points(self._middle_points_rotated, self._location))
        pygame.draw.polygon(self._surface, self._color,
                            Transform.move_points(self._front_wheel_points_rotated, self._location))
        for line in Transform.move_lines(self._middle_lines_rotated, self._location):
            pygame.draw.line(self._surface, Colors.BLACK, line[0], line[1], 1)
        pygame.draw.polygon(self._surface, Colors.BLACK,
                            Transform.move_points(self._driver_window_points_rotated, self._location))
        
        self._middle_lines_rotated_location = Transform.move_lines(self._middle_lines_rotated, self._location)

    def is_alive(self):
        return self._alive
    
    def set_alive(self, alive):
        self._alive = alive

    def set_color(self, color):
        self._color = color
        
    def get_color(self):
        return self._color
    
    def set_size(self, size):
        self._size = size
        
    def get_size(self):
        return self._size
    
    def cycle_direction_left(self):
        self._direction = self._direction - 45
        if self._direction < 0:
            self._direction = 315
        radians = math.radians(self._direction - 135)
        self._cos = math.cos(radians)
        self._sin = math.sin(radians)
        self._trail.add_turn_location(self._location)
        self._update_cycle_rotation()
        self._update_cycle_surface()
        
    def cycle_direction_right(self):
        self._direction = self._direction + 45
        if self._direction > 315:
            self._direction = 0
        radians = math.radians(self._direction - 135)
        self._cos = math.cos(radians)
        self._sin = math.sin(radians)
        self._trail.add_turn_location(self._location)
        self._update_cycle_rotation()
        self._update_cycle_surface()

    def set_direction(self, direction):
        self._direction = direction
        radians = math.radians(self._direction - 135)
        self._cos = math.cos(radians)
        self._sin = math.sin(radians)
        self._update_cycle_rotation()
        self._update_cycle_surface()
        
    def get_direction(self):
        return self._direction
        
    def set_location(self, location):
        self._location = location
        self._update_cycle_surface()
        if self._location[0] < 0 or self._location[0] > Settings.BOARD_DIMENSIONS[0]:
            self._alive = False
            return
        if self._location[1] < 0 or self._location[1] > Settings.BOARD_DIMENSIONS[1]:
            self._alive = False
        
    def get_location(self):
        return self._location
    
    def set_speed(self, speed):
        self._speed = speed
        
    def get_speed(self):
        return self._speed
    
    def raise_speed(self):
        self._speed = self._speed + self._speed_adjustment
        if self._speed > Settings.LIGHT_MAX_SPEED: 
            self._speed = Settings.LIGHT_MAX_SPEED
        
    def lower_speed(self):
        self._speed = self._speed - self._speed_adjustment
        if self._speed < Settings.LIGHT_MIN_SPEED: 
            self._speed = Settings.LIGHT_MIN_SPEED
                
    def move_tick(self, time_passed):
        if self._is_ai:
            self._ai_update_move()
        
        speed = self._speed * time_passed * self._pixel_per_time_passed
        self._location[0] += speed * self._cos - speed * self._sin
        self._location[1] += speed * self._sin + speed * self._cos
        
        # start = time.clock()
        
        self._trail.update_trail(self._location)
        
        # print "update_trail: " + str((time.clock() - start) * 1000)
        # start = time.clock()
        
        self._update_cycle_surface()
        
        # print "_update_arrow_surface: " + str((time.clock() - start) * 1000)
        
        if self._location[0] < 0 or self._location[0] > Settings.BOARD_DIMENSIONS[0]:
            self._alive = False
            return
        if self._location[1] < 0 or self._location[1] > Settings.BOARD_DIMENSIONS[1]:
            self._alive = False

    def get_surface(self):
        return self._arrow_surface


    # collision
    def collision(self, cycle):
        if not cycle._alive:
            return
            
        self._trail_collision(cycle)
        if self == cycle:
            return
        self._cycle_collision(cycle)
    
    def _cycle_collision(self, cycle):
        if Collision.intersect_lines_to_lines(self._middle_lines_rotated_location, cycle._middle_lines_rotated_location):
            self._alive = False
    
    def _trail_collision(self, cycle):
        if self._trail.collision(self._middle_lines_rotated_location, cycle._trail, cycle._location):
            self._alive = False


    # trail
    def set_trail_color(self, color):
        self._trail.set_trail_color(color)
        
    def get_trail_color(self):
        return self._trail.get_trail_color()

    def toggle_trail(self):
        self._trail.toggle_trail(self._location)
    
    def set_trail_on(self):
        self._trail.set_trail_on(self._location)
        
    def set_trail_off(self):
        self._trail.set_trail_off(self._location)
        
    def is_trail_on(self):
        return self._trail.is_trail_on()
    
    def delete_trail(self, trail):
        self._trail.delete_trail()
        
    def get_trail_surface(self):
        return self._trail.get_trail_surface()
    

    # ai
    def set_ai(self, is_ai):
        self._is_ai = is_ai
    
    def _ai_update_move(self):
        self._ai_tick += 1
        
        if self._ai_tick < self._ai_wait:
            return
        
        self._ai_tick = 0
        self._ai_wait = randint(1, 200)
        
        if randint(0, 9) > 4: 
            self.cycle_direction_left()
        else:
            self.cycle_direction_right()     

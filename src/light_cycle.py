
import math
import pygame

from settings import Settings
from colors import Colors
from cycle_trail import Cycle_trail
from rotation import Rotation
from transform import Transform
from collision import Collision


class Light_cycle():
    
    ANGLE = math.cos(math.radians(45))
    DIRECTION_UP = 0
    DIRECTION_UP_RIGHT = 45
    DIRECTION_RIGHT = 90
    DIRECTION_DOWN_RIGHT = 135
    DIRECTION_DOWN = 180
    DIRECTION_DOWN_LEFT = 225
    DIRECTION_LEFT = 270
    DIRECTION_UP_LEFT = 315
    
    def __init__(self):
        self._pixel_per_time_passed = 1.0 / 200.0
        self._speed_adjustment = 1.0
        self._color = Colors.STEELBLUE
        self._size = Settings.LIGHT_CYCLE_SIZE
        self._max_size = max(self._size[0], self._size[1])
        self._direction = self.DIRECTION_UP
        self._alive = True
        self._location = [Settings.BOARD_DIMENSIONS[0] / 2.0, Settings.BOARD_DIMENSIONS[1] / 2.0]
        self._speed = 10.0
        self._create_arrow_points()
        self._create_arrow_surface()
        self._update_arrow_surface()
        self._trail = Cycle_trail()
    
    def _create_arrow_points(self):
        # create up arrow starting in lower left and going clockwise with bottom middle at 0, 0
        self._arrow_points = (
                              # base left
                              (-self._size[0] / 4.0 , 0.0),
                              # inside left
                              (-self._size[0] / 4.0 , -self._size[1] * 3.0 / 4.0),
                              # far left
                              (-self._size[0] / 2.0 , -self._size[1] * 3.0 / 4.0),
                              # point
                              (0.0, -self._size[1]),
                              # far right
                              (self._size[0] / 2.0 , -self._size[1] * 3.0 / 4.0),
                              # inside right
                              (self._size[0] / 4.0 , -self._size[1] * 3.0 / 4.0),
                              # base right
                              (self._size[0] / 4.0 , 0.0),
                              )
        
        self._arrow_lines = []
        for i in range(len(self._arrow_points) - 1):
            self._arrow_lines.append((self._arrow_points[i], self._arrow_points[i + 1]))
        self._arrow_lines.append((self._arrow_points[len(self._arrow_points) - 1], self._arrow_points[0]))
        self._arrow_lines = tuple(self._arrow_lines)
        
        self._arrow_points_rotated = self._arrow_points
        self._arrow_lines_rotated = self._arrow_lines
    
    def _create_arrow_surface(self):
        self._arrow_surface = pygame.Surface(Settings.BOARD_DIMENSIONS)
        self._arrow_surface.set_colorkey(Colors.BLACK)
    
    def _update_arrow_surface(self):
        self._arrow_surface.fill(Colors.BLACK)
        pygame.draw.polygon(self._arrow_surface, self._color,
                            Transform.move_points(self._arrow_points_rotated, self._location))
        self._arrow_lines_rotated_location = Transform.move_lines(self._arrow_lines_rotated, self._location)

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
        self._trail.add_turn_location(self._location)
        self._arrow_points_rotated = Rotation.rotate_points(self._arrow_points, self._direction, (0, 0), (0, 0))
        self._arrow_lines_rotated = Rotation.rotate_lines(self._arrow_lines, self._direction, (0, 0), (0, 0))
        self._update_arrow_surface()
        
    def cycle_direction_right(self):
        self._direction = self._direction + 45
        if self._direction > 315:
            self._direction = 0
        self._trail.add_turn_location(self._location)
        self._arrow_points_rotated = Rotation.rotate_points(self._arrow_points, self._direction, (0, 0), (0, 0))
        self._arrow_lines_rotated = Rotation.rotate_lines(self._arrow_lines, self._direction, (0, 0), (0, 0))
        self._update_arrow_surface()

    def set_direction(self, direction):
        self._direction = direction
        self._arrow_points_rotated = Rotation.rotate_points(self._arrow_points, self._direction, (0, 0), (0, 0))
        self._arrow_lines_rotated = Rotation.rotate_lines(self._arrow_lines, self._direction, (0, 0), (0, 0))
        self._update_arrow_surface()
        
    def get_direction(self):
        return self._direction
        
    def set_location(self, location):
        self._location = location
        self._update_arrow_surface()
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
        speed = self._speed * time_passed * self._pixel_per_time_passed
        radians = math.radians(self._direction - 135)
        cos = math.cos(radians)
        sin = math.sin(radians)
        self._location[0] += speed * cos - speed * sin
        self._location[1] += speed * sin + speed * cos
        self._trail.update_trail(self._location)
        self._update_arrow_surface()
        if self._location[0] < 0 or self._location[0] > Settings.BOARD_DIMENSIONS[0]:
            self._alive = False
            return
        if self._location[1] < 0 or self._location[1] > Settings.BOARD_DIMENSIONS[1]:
            self._alive = False

    def get_surface(self):
        return self._arrow_surface


    # collision
    def collision(self, cycle):
        self._trail_collision(cycle)
        if self == cycle:
            return
        self._cycle_collision(cycle)
    
    def _cycle_collision(self, cycle):
        if Collision.intersect_lines_to_lines(self._arrow_lines_rotated_location, cycle._arrow_lines_rotated_location):
            self._alive = False
    
    def _trail_collision(self, cycle):
        if self._trail.collision(self._arrow_lines_rotated_location, cycle._trail):
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
    

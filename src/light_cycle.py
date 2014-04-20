
import math
import pygame

from settings import Settings
from colors import Colors
from cycle_trail import Cycle_trail

class Light_cycle(pygame.sprite.Sprite):
    
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
        pygame.sprite.Sprite.__init__(self)
        self._pixel_per_time_passed = 1.0 / 200.0
        self._speed_adjustment = 1.0
        self._color = Colors.STEELBLUE
        self._size = Settings.LIGHT_CYCLE_SIZE
        self._max_size = max(self._size[0], self._size[1])
        self._direction = self.DIRECTION_UP
        self._alive = True
        self._location = [100.0, 100.0]
        self._speed = 10.0
        self._create_arrow_points()
        self._create_arrow_surface()
        self._update_arrow_surface()
        self._trail = Cycle_trail()
    
    def _create_arrow_points(self):
        # create up arrow starting in lower left and going clockwise
        self._arrow_points = (
                              # base left
                              (self._max_size / 2 - self._size[0] / 4, self._max_size / 2 + self._size[1] / 2),
                              # inside left
                              (self._max_size / 2 - self._size[0] / 4, self._max_size / 2 - self._size[1] / 4),
                              # far left
                              (self._max_size / 2 - self._size[0] / 2, self._max_size / 2 - self._size[1] / 4),
                              # point
                              (self._max_size / 2, self._max_size / 2 - self._size[1] / 2),
                              # far right
                              (self._max_size / 2 + self._size[0] / 2, self._max_size / 2 - self._size[1] / 4),
                              # inside right
                              (self._max_size / 2 + self._size[0] / 4, self._max_size / 2 - self._size[1] / 4),
                              # base right
                              (self._max_size / 2 + self._size[0] / 4, self._max_size / 2 + self._size[1] / 2),
                              )
    
    def _create_arrow_surface(self):
        self._arrow_surface = pygame.Surface((self._max_size, self._max_size))
        self._arrow_surface.set_colorkey(Colors.BLACK)
    
    def _update_arrow_surface(self):
        self._arrow_surface.fill(Colors.BLACK)
        pygame.draw.polygon(self._arrow_surface, self._color, self._arrow_points)
        self._arrow_surface_rotated = pygame.transform.rotate(self._arrow_surface, -self._direction)

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
        self._update_arrow_surface()
        
    def cycle_direction_right(self):
        self._direction = self._direction + 45
        if self._direction > 315:
            self._direction = 0
        self._trail.add_turn_location(self._location)
        self._update_arrow_surface()

    def set_direction(self, direction):
        self._direction = direction 
        
    def get_direction(self):
        return self._direction
        
    def set_location(self, location):
        self._location = location
        
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
        self._location[0] = self._location[0] + speed * cos - speed * sin
        self._location[1] = self._location[1] + speed * sin + speed * cos
        self._trail.update_trail(self._location)    

    def get_surface(self):
        return self._arrow_surface_rotated
    
    def get_surface_location(self):
        # TODO: Is there a better math way to do this?
        if self._direction == self.DIRECTION_UP:
            return (self._location[0] - self._max_size / 2, self._location[1] - self._max_size)    
        elif self._direction == self.DIRECTION_UP_RIGHT:
            return (self._location[0] - self._max_size / 2 * self.ANGLE, self._location[1] - self._max_size)
        elif self._direction == self.DIRECTION_RIGHT:
            return (self._location[0], self._location[1] - self._max_size / 2)
        elif self._direction == self.DIRECTION_DOWN_RIGHT:
            return (self._location[0] - self._max_size / 2 * self.ANGLE, self._location[1] - self._max_size / 2 * self.ANGLE)
        elif self._direction == self.DIRECTION_DOWN:
            return (self._location[0] - self._max_size / 2, self._location[1])
        elif self._direction == self.DIRECTION_DOWN_LEFT:
            return (self._location[0] - self._max_size, self._location[1] - self._max_size / 2 * self.ANGLE)
        elif self._direction == self.DIRECTION_LEFT:
            return (self._location[0] - self._max_size, self._location[1] - self._max_size / 2)
        elif self._direction == self.DIRECTION_UP_LEFT:
            return (self._location[0] - self._max_size, self._location[1] - self._max_size)
        else:
            raise Exception("Invalid direction")

    def _rotate(self, points):
        # not used at this time
        radians = math.radians(self._direction)
        cos = math.cos(radians)
        sin = math.sin(radians)
        return (points[0] * cos - points[1] * sin,
                points[0] * sin + points[1] * cos)


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
    

import pygame

from colors import Colors
from collision import Collision


class Cycle_trail():
    
    def __init__(self, surface):
        self._surface = surface
        self._trail = []
        self._trail_start_location = None
        self._trail_on = False
        self._color = Colors.STEELBLUE
    
    def _update_trail_surface(self, location=None):
        if self._trail != []:
            for line in self._trail:
                pygame.draw.line(self._surface, self._color, line[0], line[1], 2)
        if location is None:
            return
        if not self._trail_on:
            return
        pygame.draw.line(self._surface, self._color, self._trail_start_location, tuple(location), 2)
        
    def set_trail_color(self, color):
        self._color = color
        
    def get_trail_color(self):
        return self._color
        
    def delete_trail (self):
        self._trail = []
        self._update_trail_surface()

    def add_turn_location (self, location):
        if not self._trail_on:
            return
        self._trail.append((self._trail_start_location, tuple(location)))
        self._trail_start_location = tuple(location)
    
    def add_location (self, location1, location2):
        self._trail.append((tuple(location1), tuple(location2)))
        
    def toggle_trail(self, location):
        if self._trail_on:
            self.set_trail_off(location)
        else:
            self.set_trail_on(location)
    
    def set_trail_on(self, location):
        self._trail_on = True
        self._trail_start_location = tuple(location)
    
    def set_trail_off(self, location):
        if self._trail_on:
            self._trail.append((self._trail_start_location, tuple(location)))
            self._update_trail_surface()
        self._trail_on = False
        
    def is_trail_on(self):
        return self._trail_on
    
    def update_trail(self, location):
        self._update_trail_surface(location)
        
    def get_trail_surface(self):
        return self._trail_surface
    
    # collision
    def collision(self, arrow_lines_rotated_location, cycle_trail, location):
        if Collision.intersect_lines_to_lines(arrow_lines_rotated_location, cycle_trail._trail):
            return True
        if not cycle_trail._trail_on:
            return False
        if self == cycle_trail:
            return False
        if Collision.intersect_lines_to_lines(arrow_lines_rotated_location, [(cycle_trail._trail_start_location, tuple(location))]):
            return True
        return False

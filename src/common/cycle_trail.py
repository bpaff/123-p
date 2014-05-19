
pygame_failed = True
try:
    import pygame
    pygame_failed = False
except:
    pass

from colors import Colors
from common.messages import Messages
from collision import Collision


class Cycle_trail():
    
    def __init__(self, surface, cycle_number, is_server):
        self._surface = surface
        self._cycle_number = cycle_number
        self._is_server = is_server
        self._trail = []
        self._trail_start_location = None
        self._trail_on = False
        if not is_server:
            self._color = Colors.STEELBLUE
        self._messages = []
    
    
    def update_trail_surface(self, location=None):
        if self._surface is None:
            return
        if self._trail != []:
            for line in self._trail:
                pygame.draw.line(self._surface, self._color, line[0], line[1], 2)
        if location is None:
            return
        if not self._trail_on:
            return
        pygame.draw.line(self._surface, self._color, self._trail_start_location, tuple(location), 2)
    
    
    def get_and_delete_messages(self):
        messages = self._messages
        self._messages = []
        return messages
    
    
    def set_trail_color(self, color):
        self._color = color


    def add_turn_location (self, location):
        if not self._trail_on:
            return
        if self._trail_start_location[0] == location[0] and self._trail_start_location[1] == location[1]: 
            return
        self._trail.append((self._trail_start_location, tuple(location)))
        self._trail_start_location = tuple(location)
        if self._is_server:
            self._messages.append(Messages.trail_turn(self._cycle_number, tuple(location)))

    
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
        if self._is_server:
            self._messages.append(Messages.trail_on(self._cycle_number, self._trail_on, self._trail_start_location))

    
    def set_trail_off(self, location):
        if self._trail_on:
            self._trail.append((self._trail_start_location, tuple(location)))
        self._trail_on = False
        if self._is_server:
            self._messages.append(Messages.trail_on(self._cycle_number, self._trail_on, tuple(location)))

        
    def is_trail_on(self):
        return self._trail_on

    
    # collision
    def collision(self, lines, cycle_trail, location):
        if Collision.intersect_lines_to_lines(lines, cycle_trail._trail):
            return True
        if not cycle_trail._trail_on:
            return False
        if self == cycle_trail:
            return False
        if Collision.intersect_lines_to_lines(lines, ((cycle_trail._trail_start_location, location),)):
            return True
        return False


    def collision_lines_with_trail(self, lines, location, cycle_number): 
        if Collision.intersect_lines_to_lines(lines, self._trail):
            return True
        if not self._trail_on:
            return False
        if self._cycle_number == cycle_number:
            return False
        if Collision.intersect_lines_to_lines(lines, ((self._trail_start_location, location),)):
            return True
        return False

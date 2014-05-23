
import math
pygame_failed = True
try:
    import pygame
    pygame_failed = False
except:
    pass

from common.settings import Settings
from common.colors import Colors
from common.messages import Messages
from common.cycle_trail import Cycle_trail
from common.rotation import Rotation
from common.transform import Transform
from common.collision import Collision


class Light_cycle():
    
    def __init__(self, surface, cycle_number, is_server):
        self._surface = surface
        self._cycle_number = cycle_number
        self._is_server = is_server
        self._speed = Settings.LIGHT_START_SPEED
        self._speed_adjustment = Settings.LIGHT_SPEED_ADJUSTMENT
        if not is_server:
            self._color = Colors.STEELBLUE
        self._size = Settings.LIGHT_CYCLE_SIZE
        self._max_size = max(self._size[0], self._size[1])
        self._direction = 0
        self._alive = True
        self._location = [100, 100]
        self._update_degress()
        self._update_cycle_rotation()
        self.update_cycle_surface()
        self._trail = Cycle_trail(surface, cycle_number, self._is_server)
        self._messages = []
        self._cycle_wall_off_time = 0
    
    
    def _update_degress(self):
        radians = math.radians(self._direction - 135)
        self._cos = math.cos(radians)
        self._sin = math.sin(radians)
    
    
    def _update_cycle_rotation(self):
        self._back_wheel_points_rotated = Rotation.rotate_points(Settings.BACK_WHEEL_POINTS, self._direction, (0, 0), (0, 0))
        self._middle_points_rotated = Rotation.rotate_points(Settings.MIDDLE_POINTS, self._direction, (0, 0), (0, 0))
        self._front_wheel_points_rotated = Rotation.rotate_points(Settings.FRONT_WHEEL_POINTS, self._direction, (0, 0), (0, 0))
        self._middle_lines_rotated = Rotation.rotate_lines(Settings.MIDDLE_LINES, self._direction, (0, 0), (0, 0))
        self._driver_window_points_rotated = Rotation.rotate_points(Settings.DRIVER_WINDOW_POINTS, self._direction, (0, 0), (0, 0))
        
        self._middle_lines_rotated_location = Transform.move_lines(self._middle_lines_rotated, self._location)
    
    
    def update_cycle_surface(self):
        if self._surface is None:
            return
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
    
    
    def get_cycle_position(self):
        return {'direction':self._direction, 'location':self._location}
    
    
    def set_cycle_position(self, info):
        self.set_direction(info['direction'])
        self.set_location(info['location'])
    
    
    def get_speed(self):
        return self._speed

    
    def get_and_delete_messages(self):
        messages = self._messages
        self._messages = []
        return messages
    

    def is_alive(self):
        return self._alive

    
    def set_alive(self, alive):
        self._alive = alive
        self._messages.append(Messages.cycle_alive(self._cycle_number, self._alive))


    def set_color(self, color):
        self._color = color

    
    def turn_left(self):
        self._direction -= 45
        if self._direction < 0:
            self._direction = 315
        self._update_degress()
        self._trail.add_turn_location(self._location)
        self._update_cycle_rotation()


    def turn_right(self):
        self._direction += 45
        if self._direction > 315:
            self._direction = 0
        self._update_degress()
        self._trail.add_turn_location(self._location)
        self._update_cycle_rotation()


    def set_direction(self, direction):
        self._direction = direction
        self._update_degress()
        self._update_cycle_rotation()

        
    def set_location(self, location):
        self._location = list(location)
        if self._location[0] < 0 or self._location[0] > Settings.BOARD_DIMENSIONS[0]:
            self.set_alive(False)
            return
        if self._location[1] < 0 or self._location[1] > Settings.BOARD_DIMENSIONS[1]:
            self.set_alive(False)
            return

    
    def raise_speed(self):
        self._speed = self._speed + self._speed_adjustment
        if self._speed > Settings.LIGHT_MAX_SPEED: 
            self._speed = Settings.LIGHT_MAX_SPEED

        
    def lower_speed(self):
        self._speed = self._speed - self._speed_adjustment
        if self._speed < Settings.LIGHT_MIN_SPEED: 
            self._speed = Settings.LIGHT_MIN_SPEED

                
    def move_tick(self, time_passed):
        if not self._trail.is_trail_on():
            self._cycle_wall_off_time += time_passed
            if self._cycle_wall_off_time > 5.0:
                self.set_trail_on(self._location)
                
        speed = self._speed * time_passed
        self._location[0] += speed * self._cos - speed * self._sin
        self._location[1] += speed * self._sin + speed * self._cos
        
        self._middle_lines_rotated_location = Transform.move_lines(self._middle_lines_rotated, self._location)
        
        if self._location[0] < 0 or self._location[0] > Settings.BOARD_DIMENSIONS[0]:
            self.set_alive(False)
            return
        if self._location[1] < 0 or self._location[1] > Settings.BOARD_DIMENSIONS[1]:
            self.set_alive(False)
            return
        
        self._messages.append(Messages.cycle_position(self._cycle_number, self.get_cycle_position()))


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
            self.set_alive(False)


    def _trail_collision(self, cycle):
        if self._trail.collision(self._middle_lines_rotated_location, cycle._trail, cycle._location):
            self.set_alive(False)


    def collision_lines(self, lines, cycle_number):
        if not self._alive:
            return False
        
        if self._trail.collision_lines_with_trail(lines, self._location, cycle_number):
            return True
        
        if self._cycle_number == cycle_number:
            return False
        
        return Collision.intersect_lines_to_lines(lines, self._middle_lines_rotated_location)
    

    # trail
    def trail_get_and_delete_messages(self):
        return self._trail.get_and_delete_messages()
    
    
    def update_trail_surface(self):
        self._trail.update_trail_surface(self._location)


    def set_trail_turn(self, location):
        self._trail.add_turn_location(location)    
    
    
    def set_trail_color(self, color):
        self._trail.set_trail_color(color)


    def toggle_trail(self):
        if self._trail.is_trail_on():
            self.set_trail_off(None)
        else:
            self.set_trail_on(None)


    def set_trail_on(self, location):
        self._cycle_wall_off_time = 0
        if location is None:
            self._trail.set_trail_on(self._location)
        else:
            self._trail.set_trail_on(location) 


    def set_trail_off(self, location):
        if location is None:
            self._trail.set_trail_off(self._location)
        else:
            self._trail.set_trail_off(location) 


    def is_trail_on(self):
        return self._trail.is_trail_on()

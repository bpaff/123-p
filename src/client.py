
import pygame

from settings import Settings
from colors import Colors
from light_cycle import Light_cycle


class Client():
    
    def __init__(self):
        self._pygame_setup()
        self._game_setup()
    
    def _pygame_setup(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._surface = pygame.display.set_mode(Settings.SCREEN_DIMENSIONS)
        pygame.display.set_caption(Settings.CAPTION)
        pygame.mouse.set_visible(False)
        
    def _game_setup(self):
        self._keep_running = True
        self._time_passed_history = [0, 0, 0, 0]
        self._number_of_players = 1
        self._light_cycles = {}
        self._light_cycles[0] = Light_cycle()
        self._light_cycles[1] = Light_cycle()
#         self._light_cycles[2] = Light_cycle()
        self._light_cycles[1].set_color(Colors.BLUEVIOLET)
        self._light_cycles[1].set_location([600.0, 20.0])
        self._light_cycles[1].set_direction(Light_cycle.DIRECTION_DOWN_LEFT)
#         self._light_cycles[2].set_color(Colors.DARKGREEN)
#         self._light_cycles[2].set_location([160.0, 100.0])
#         self._light_cycles[2].cycle_direction_right()
    
    def run(self):
        while self._keep_running:
            # time_passed in ms
            self._time_passed = self._clock.tick(Settings.TICK) 
            self._get_input()
            self._update_objects()
            self._update_display()
            
    def _get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._keep_running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    self._keep_running = False
                elif key == pygame.K_UP:
                    self._light_cycles[0].raise_speed()
                elif key == pygame.K_DOWN:
                    self._light_cycles[0].lower_speed()
                elif key == pygame.K_LEFT:
                    self._light_cycles[0].cycle_direction_left()
                elif key == pygame.K_RIGHT:
                    self._light_cycles[0].cycle_direction_right()
                elif key == pygame.K_a:
                    self._light_cycles[0].raise_speed()
                elif key == pygame.K_z:
                    self._light_cycles[0].lower_speed()
                elif key == pygame.K_SPACE:
                    self._light_cycles[0].toggle_trail()
                
    def _update_objects(self):
        self._update_time_passed_history()
        
        for cycle in self._light_cycles.itervalues():
            cycle.move_tick(self._time_passed)
        for cycle1 in self._light_cycles.itervalues():
            for cycle2 in self._light_cycles.itervalues():
                cycle1.collision(cycle2)
        
         
    def _update_time_passed_history(self):
        self._time_passed_history[3] = self._time_passed_history[2]
        self._time_passed_history[2] = self._time_passed_history[1]
        self._time_passed_history[1] = self._time_passed_history[0]
        self._time_passed_history[0] = self._time_passed
        self._time_passed_avg = float(sum(self._time_passed_history)) / len(self._time_passed_history)
        
    def _update_display(self):
        self._surface.fill(Colors.BLACK)
        
#         font_monospace = pygame.font.SysFont("monospace", 24)
#         text = font_monospace.render('FPS: ' + str(int(1000 / self._time_passed_avg)), 1, Colors.ANTIQUEWHITE)
#         self._surface.blit(text, (100, 100))
        
        for cycle in self._light_cycles.itervalues():
            if cycle.is_alive():
                self._surface.blit(cycle.get_surface(), (0, 0))
                self._surface.blit(cycle.get_trail_surface(), (0, 0))
            
        pygame.display.update()


client = Client()

client.run()

pygame.quit()



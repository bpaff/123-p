
import time
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
        self._start = time.clock()
        self._keep_running = True
        self._number_of_players = 1
        self._light_cycles = {}
        self._light_cycles[0] = Light_cycle(self._surface)
        self._light_cycles[1] = Light_cycle(self._surface)
        self._light_cycles[1].set_color(Colors.BLUEVIOLET)
        self._light_cycles[1].set_location([700.0, 100.0])
        self._light_cycles[1].set_direction(Light_cycle.DIRECTION_DOWN_LEFT)
        self._light_cycles[1].set_trail_color(Colors.BLUEVIOLET)
        self._light_cycles[1].set_trail_on()
        self._light_cycles[1].set_ai(True)
        self._light_cycles[2] = Light_cycle(self._surface)
        self._light_cycles[2].set_color(Colors.DARKGREEN)
        self._light_cycles[2].set_location([700.0, 400.0])
        self._light_cycles[2].set_direction(Light_cycle.DIRECTION_UP_LEFT)
        self._light_cycles[2].set_trail_color(Colors.DARKGREEN)
        self._light_cycles[2].set_trail_on()
        self._light_cycles[2].set_ai(True)
        self._light_cycles[3] = Light_cycle(self._surface)
        self._light_cycles[3].set_color(Colors.GOLD)
        self._light_cycles[3].set_location([100.0, 400.0])
        self._light_cycles[3].set_direction(Light_cycle.DIRECTION_UP_RIGHT)
        self._light_cycles[3].set_trail_color(Colors.GOLD)
        self._light_cycles[3].set_trail_on()
        self._light_cycles[3].set_ai(True)

    
    def run(self):
        while self._keep_running:
            # time_passed in ms
            self._time_passed = self._clock.tick(Settings.TICK) 
            self._get_input()
            self._update_objects()
            
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
        self._surface.fill(Colors.BLACK)
        
        self._start = time.clock()
                
        for cycle in self._light_cycles.itervalues():
            if cycle.is_alive():
                cycle.move_tick(self._time_passed)
        
        for cycle1 in self._light_cycles.itervalues():
            if cycle1.is_alive():
                for cycle2 in self._light_cycles.itervalues():
                    cycle1.collision(cycle2)
        
        print "tick: " + str((time.clock() - self._start) * 1000)
                    
        pygame.display.update()
        
#         font_monospace = pygame.font.SysFont("monospace", 24)
#         text = font_monospace.render('FPS: ' + str(int(1 / self._time_passed_avg)), 1, Colors.ANTIQUEWHITE)
#         self._surface.blit(text, (50, 550))


client = Client()

client.run()

pygame.quit()



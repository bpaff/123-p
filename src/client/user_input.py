
import pygame


from common.messages import Messages


class User_input():
    
    def __init__(self, game):
        self._game = game
        self._messages = []
        

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.send_quit()
                self._game.stop()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._game.send_quit()
                    self._game.stop()
                    break
                elif event.key == pygame.K_UP:
                    self._messages.append(Messages.player_input('up'))
                elif event.key == pygame.K_DOWN:
                    self._messages.append(Messages.player_input('down'))
                elif event.key == pygame.K_LEFT:
                    self._messages.append(Messages.player_input('left'))
                elif event.key == pygame.K_RIGHT:
                    self._messages.append(Messages.player_input('right'))
                elif event.key == pygame.K_a:
                    self._messages.append(Messages.player_input('up'))
                elif event.key == pygame.K_z:
                    self._messages.append(Messages.player_input('down'))
                elif event.key == pygame.K_SPACE:
                    self._messages.append(Messages.player_input('space'))
        
        
    def get_and_delete_messages(self):
        messages = self._messages
        self._messages = []
        return messages


    def get_text_input(self):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return 'quit'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'quit'
            if event.key == pygame.K_BACKSPACE:
                return 'backspace'
            if event.key == pygame.K_RETURN:
                return 'return'
            if event.key == pygame.K_KP_ENTER:
                return 'return'
            return event.unicode

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 17:53:00 2020

@author: User
"""

import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion():
    """ A class to manage the overall game behaviours """
    
    def __init__(self):
        """ initializes background settings that pygame needs to work properly """
        pygame.init()
        
        self.settings=Settings()
        
        self.screen=pygame.display.set_mode((self.settings.window_width,self.settings.window_height))
        pygame.display.set_caption("Alien Invasion")
        
        self.ship=Ship(self)

    def run_game(self):
        """Starting the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()
            
    def _check_events(self):
        """ watching for the keyboard and mouse events """
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    """Move the ship to the right (but it's not continuous)"""
                    self.ship.rect.x += 10
    
    def _update_screen(self):
        """ update what's visible """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()
    
if __name__=='__main__':
    #Making a game insatnce, and running the game by using run_game method
    ai=AlienInvasion()
    ai.run_game()
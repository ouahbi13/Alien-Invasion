# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:44:57 2020

@author: User
"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A Class representing the alien """
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        #Loading the image representing an alien and set its rect attribute
        #self.image = pygame.image.load(os.path.join(filepath,'graphic-3744115_1280.bmp'))
        self.image = pygame.image.load('images/alien_3-removebg-preview.png')
        self.image = pygame.transform.scale(self.image,(50,50))
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect = self.image.get_rect()
        
        #Start each alien at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Store the alien's exact horizontal position
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return True if an alien reach the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """Update the alien's position"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 19:15:25 2020

@author: User
"""

import pygame

class Ship:
    """ A class to control the ship """
    
    def __init__(self,ai_game):
        """ Initializing the ship and setting its position """
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        
        """ loading the ship image and getting its rect """
        self.image=pygame.image.load('images/36-363746_spaceship-png-pic-png-mart-commercial-clip-art.png')
        self.image=pygame.transform.scale(self.image,(40,50))
        self.rect=self.image.get_rect()
        
        
        """ setting the ship initially at the bottom center of the screen """
        self.rect.midbottom=self.screen_rect.midbottom
        
        #Movement flag
        self.moving_right=False
    
    def update(self):
        if self.moving_right:
            self.rect.x += 1
    
    def blitme(self):
        """Drawing the ship at its current location"""
        self.screen.blit(self.image,self.rect)
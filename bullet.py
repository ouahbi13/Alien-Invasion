# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 20:36:00 2020

@author: User
"""

import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A Class to represent the bullets"""
    def __init__(self,ai_game):
        """ Create a bullet object at the ship's current position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        #Create a bullet rect at (0,0) and then set correct positon
        self.rect = pg.Rect((0,0,self.settings.bullet_width,self.settings.bullet_height))
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #Set the bullet's position as a decimal value
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet up"""
        #Decrease th decimal position of the bullet
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Drawing the bullet"""
        pg.draw.rect(self.screen,self.color,self.rect)
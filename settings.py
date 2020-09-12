# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 18:48:36 2020

@author: User
"""
import pygame

class Settings:
    """ A class to store game settings """
    def __init__(self):
        self.window_width = 900
        self.window_height = 700
        self.bg_color = (255,255,255)
        pygame.display.set_mode((self.window_width,self.window_height))
        self.bg = pygame.image.load('images/starfield.png').convert()
        self.bg = pygame.transform.scale(self.bg,(self.window_width,self.window_height))

        #Ship settings
        self.ship_limit = 3
        #Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 30
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 100
        #Alien Settings
        self.fleet_drop_speed = 10
        #How quick the game speeds up
        self.speedup_scale = 1.1
        #How much the alien points increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Iinitialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # 1 represents right -1 represents left
        self.fleet_direction = 1
        
        #Scoring points
        self.alien_points = 50
        
    def increase_speed(self):
        """Increase overall speed and alien points"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        #Increase alien points in each level
        self.alien_points = int(self.alien_points * self.score_scale)       
        
                
        
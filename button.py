# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:42:36 2020

@author: User
"""

import pygame.font

class Button:
    
    def __init__(self,ai_game,msg):
        """The button's attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #Define the button's dimensions and properties
        self.width,self.height = 200,50
        self.button_color = (0,0,255)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)
        
        #Set the rect and center it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        
        self._prep_msg(msg)
    
    def _prep_msg(self,msg):
        """Turn msg to a renderd image and center text on the button"""
        self.msg_image = self.font.render(msg,True,self.text_color,
                                            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        #Draw blank button and draw the msg
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
        
        
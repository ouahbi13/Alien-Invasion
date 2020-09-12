# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 20:26:46 2020

@author: User
"""


class GameStats:
    """A Class to track statistics for Alien Invasion"""
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_game()
        #the game state is initially set to inactive
        self.game_active = False
        #High score is never reset
        self.high_score = self._read_high_score()
        
    def reset_game(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    
    def _read_high_score(self):
        with open("C:\\Users\\User\\Desktop\\Alien Invasion\\highscore.txt") as f:
            high_score = int(f.read())
            return high_score
        
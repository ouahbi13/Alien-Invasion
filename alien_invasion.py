# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 17:53:00 2020

@author: User
"""

import sys

from time import sleep

import pygame

import pygame.mask

import pygame.mixer

from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion():
    """ A class to manage the overall game behavior """
    
    def __init__(self):
        """ initializes background settings that pygame needs to work properly """
        pygame.init()
        
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.window_width,self.settings.window_height))
        
        """Set to full screen mode"""
        #self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.window_width=self.screen.get_rect().width
        #self.settings.window_height=self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")
        
        #An instance to create game statistics
        self.stats = GameStats(self)
        
        #Create a scoreboard
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        #Make a Play button
        self.play_button = Button(self,"Play")

        self._set_background_music_and_sound_effects()

    def run_game(self):
        """Starting the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:   
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    
    def _set_background_music_and_sound_effects(self):
        """Audio Effects"""
        #Background Music
        self.level_1 = 'music/level-1.mp3'
        self.level_2 = 'music/level-2.mp3'
        self.level_3 = 'music/level-3.mp3'
        self.level_4 = 'music/level-4.mp3'
        self.level_5 = 'music/level-5.mp3'
        self.level_6 = 'music/level-6.mp3'
                            
        self.list = [self.level_1,self.level_2,self.level_3,self.level_4,self.level_5,self.level_6]

        self.i = 0
        
        #Sound effects
        self.ship_sound = pygame.mixer.Sound("music/Ship Hit.wav")
        self.alien_sound = pygame.mixer.Sound("music/Alien Hit.wav")
        self.bullet_sound = pygame.mixer.Sound("music/Bullet Shot.wav")
        self.game_over = pygame.mixer.Sound("music/game over.wav")


    def _check_events(self):
        """ watching for the keyboard and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_high_score()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
               self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def fire_bullet(self):
        """ Create a new bullet (only if it's allowed) and add it to the bullet group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keydown_events(self,event):
        """ Respond to key presses """ 
        if event.key == pygame.K_RIGHT:
            """Move the ship to the right (now it's contionuous)"""
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_a:
            """ To quit by pressing "Q" """
            self._save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
        
    def _check_keyup_events(self,event):
        """ Respond to key releases """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                    
    def _update_bullets(self):
        """Update bullet positions and delete disappeared bullets"""
        #Update bullet position
        self.bullets.update()
        
        #Delete old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets)) #to see how many bullets are currently on the screen 
        self._check_bullet_alien_collision()
        
    def _update_aliens(self):
        """Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        #Look for any alien ship collision 
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            if pygame.sprite.spritecollide(self.ship,self.aliens,False,pygame.sprite.collide_mask):  
            #print("Ship hit !!!")
                self.ship_sound.play()
                self._ship_hit()

        #Look of any alien reaching the bottom
        self._check_aliens_bottom()
                
    def _check_bullet_alien_collision(self):
         #Check for bullet-alien collisions
        collisions = pygame.sprite.groupcollide(
                self.bullets,self.aliens,True,True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.alien_sound.play()
            self.sb.prep_score()
            self.sb.check_high_score()
            
        if not self.aliens:
            self._start_new_level()
            
    def _start_new_level(self):
        #Destroying existing bullets and creating a new fleet
        self.bullets.empty()
        self._create_fleet()
        if self.i < 5:
            self.i += 1
            self._play_background_music(self.list[self.i])
        self.settings.increase_speed() 
        #Increase level
        self.stats.level += 1
        self.sb.prep_level()
    
        
    def _create_fleet(self):
        """A method for creating a fleet of aliens"""
        #Create an alien instance and find the number of aliens in a row
        #The space between two aliens is equal to an alien width
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.window_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        #Determine the number of rows available
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.window_height 
                                - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height) + 1

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(row_number,alien_number)
        
            
    def _create_alien(self,row_number,alien_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        
    def _check_fleet_edges(self):
        """Responds if any alien reaches the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _ship_hit(self):
        """Pause the screen when the ship is hit, decrease the ships left and reset the positions"""
        if self.stats.ships_left > 0:
           self.stats.ships_left -= 1
           
           #Update the scoreboard
           self.sb.prep_ships()
           
           #Delete any remaining aliens and bullets
           self.bullets.empty()
           self.aliens.empty()
           
           #Create a new fleet and recenter the ship
           self._create_fleet()
           self.ship._center_ship()
           sleep(1)
         
        else:
            self.stats.game_active = False
            pygame.mixer.music.stop()
            self.game_over.play()
            pygame.mouse.set_visible(True)
            
            
    def _check_aliens_bottom(self):
        """Responds to an alien reaching the ground"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom :
                self._ship_hit()
                break
            
    def _start_game(self):
        #Reset the game stats
        self.stats.reset_game()    
        self.stats.game_active = True
        self._play_background_music(self.level_1)
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        
        #Empty the screen
        self.aliens.empty()
        self.bullets.empty()
        
        #Recreate the fleet and recenter the ship
        self._create_fleet()
        self.ship._center_ship()
        
        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        
    
    def _check_play_button(self,mouse_pos):
        """Starts a new game when the player clicks the button"""
        click_button = self.play_button.rect.collidepoint(mouse_pos)
        if click_button and not self.stats.game_active:
            self._start_game()

    def _save_high_score(self):
        with open("C:\\Users\\User\\Desktop\\Alien Invasion\\highscore.txt",'w') as f:
            self.sb.prep_score()
            self.sb.check_high_score()
            f.write(str(self.stats.high_score))            
    
    def _play_background_music(self,music):
        pygame.mixer.music.load(music)
        #print(pygame.mixer.music.get_volume())
        pygame.mixer.music.set_volume(0.50)
        pygame.mixer.music.play(-1)

    def _update_screen(self):
        """ update what's visible """
        #self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.settings.bg,(0,0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #Draw scoring info
        self.sb.show_score()
        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
    
if __name__=='__main__':
    #Making a game insatnce, and running the game by using run_game method
    ai = AlienInvasion()
    ai.run_game()
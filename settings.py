# Alien Invasion
# Created by: Hector Rodriguez & Justin Castillo
import pygame
import pyautogui

class Settings():
    """A class to store all settings for ALien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.screen_width, self.screen_height = pyautogui.size()
        self.bg = pygame.image.load('images/bg.jpg').convert()
        self.bg_speed = 4
        self.bg_main_speed = 2

        # Ship settings
        self.ship_speed_factor = 5.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        
        # How quickly the alien point values increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()

        # Pause 
        self.pause = False
        self.pause_text1 = pygame.font.SysFont('monospace', 60).render('Paused', True, pygame.color.Color('White'))
        self.pause_text2 = pygame.font.SysFont('monospace', 60).render('Press SPACE When Ready', True, pygame.color.Color('White'))
        self.lives_text = pygame.font.SysFont('monospace', 30).render('LIVES', True, pygame.color.Color('Red'))
        self.score_text = pygame.font.SysFont('monospace', 30).render('SCORE:', True, pygame.color.Color('Red'))
        self.levels_text = pygame.font.SysFont('monospace', 30).render('LEVEL:', True, pygame.color.Color('Red'))
        self.high_score_text = pygame.font.SysFont('monospace', 50).render('HIGH SCORE', True, pygame.color.Color('Red'))

        # Home screen
        self.home = True
        self.title_text = pygame.font.SysFont('monospace', 100).render('Alien Invasion', True, pygame.color.Color('Green'))
        self.any_text = pygame.font.SysFont('monospace', 40).render('Press ANY Button', True, pygame.color.Color('Yellow'))
        self.version_text = pygame.font.SysFont('monospace', 20).render('Version 2.0', True, pygame.color.Color('Green'))
        self.version_credit = pygame.font.SysFont('monospace', 20).render('Credit: ', True, pygame.color.Color('Green'))
        self.version_hector = pygame.font.SysFont('monospace', 20).render('H.R.', True, pygame.color.Color('Green'))
        self.version_jason = pygame.font.SysFont('monospace', 20).render('& J.C.', True, pygame.color.Color('Green'))

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 5.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring.
        self.alien_points = 10

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
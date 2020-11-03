
# Alien Invasion
# Created by: Hector Rodriguez & Justin Castillo
import sys

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf

def run_game():
        # Initialize pygame, settings, and screen object.
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        ai_settings = Settings()
        pygame.display.set_caption("Alien Invasion")

        # Make the Play Button.
        quit_button = Button(ai_settings, screen, "Quit Game")


        # Create an instance to store game statistics and create a scoreboard.
        stats = GameStats(ai_settings)
        sb = Scoreboard(ai_settings, screen, stats)

        # Make a ship, a group of bullets, and a group of aliens.
        ship = Ship(ai_settings, screen)
        bullets = Group()
        aliens = Group()        

        # Variables to move screen.
        y = 0
        y_main = 0

        # Start loop for home screen.
        while ai_settings.home:
            # Move background.
            gf.bg_main(ai_settings, screen, y_main)

            # Display main screen.
            gf.main_screen(ai_settings, screen)

            # Check when user presses any key.
            gf.check_main_event(ai_settings, screen, stats, sb, ship, aliens, bullets)

            y_main += ai_settings.bg_main_speed


        # Create the fleet of aliens.
        gf.create_fleet(ai_settings, screen, ship, aliens)

        # Start the main loop for the game.
        while True:
            # Move background
            gf.bg_update(ai_settings, screen, sb, y)
            # Check input events
            gf.check_events(ai_settings, screen, stats, sb, quit_button, ship, aliens, bullets)
             # Draw the score information.
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets)
            y += ai_settings.bg_speed


            if stats.game_active:
                ship.update()
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

run_game()
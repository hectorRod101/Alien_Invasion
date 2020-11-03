# Alien Invasion
# Created by: Hector Rodriguez & Justin Castillo

# File path to store high score.
from os.path import abspath, dirname
BASE_PATH = abspath(dirname(__file__))
FILE_PATH = BASE_PATH + '/highscore.txt'

class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()


        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        try:
             h = open(FILE_PATH, "r")
             content = h.readline()
             self.high_score = int(content)
             h.close()
        except IOError:
            h = open(FILE_PATH, "w")
            self.high_score = 0
            h.write(str(0))
            h.close()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
    
    def write_high_score_(self, score):
        """Write to file new high score."""
        h = open(FILE_PATH, "w")
        h.write(str(score))
        h.close()
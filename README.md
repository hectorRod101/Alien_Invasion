# Alien_Invasion
[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)

## About

Alien Invasion is a take on the two-dimensional fixed shooter game Space Invaders. The player controls a ship which moves
horizontally moving across at the bottom of the screen and shots at descending alien ships. The point of the game is to defeat 
five rows of eleven alien ships that move horizontally back and forth across the screen as they advance towards the bottom of the screen. 
If the player defeats all alien ships in the current screen, the player earns points and moves onto the next wave of alien ships.

The player continuously must survive with only three lives for the entirety of the game. The only way the player loses a life if the 
alien ship reaches the bottom of the screen and collides with their ship. Each wave the alien ships get faster which makes it harder to 
aim at them.

<img src="https://i.imgur.com/fUu0j9w.png" width="700" height="500" />
<img src="https://i.imgur.com/o34EOJR.png" width="700" height="500" />

## How To Play

- If you don't have [Python](https://www.python.org/downloads/) or [Pygame](http://www.pygame.org/download.shtml) installed, you can simply double click the .exe file to play the game.
  **Note:** _The .exe file needs to stay in the same directory as the sounds, images, and font folders._

- If you have the correct version of Python and Pygame installed, you can run the program in the command prompt / terminal.

```bash
cd Alien_Invasion
python alien_invasion.py
```

**Note:** If you're using Python 3, replace the command "python" with "python3"

**MacOS Mojave**: You need to use Python 3.7.2 or greater: [Source](https://github.com/pygame/pygame/issues/555)

## Controls
```bash
Any Keys: Start Game
Left/Right Arrow Keys: Move Ship
Space Bar: Fire Laser
Press Key p: Pause
Mouse: Click
```

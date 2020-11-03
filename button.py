# Alien Invasion
# Created by: Hector Rodriguez & Justin Castillo
import pygame.font

class Button():
    def __init__(self, ai_settings, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.width_border, self.height_border = 330, 75 
        self.button_color = (0, 0, 0)
        self.button_border = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect_border = pygame.Rect(0, 0, self.width_border, self.height_border)
        self.rect.center = ((ai_settings.screen_width/2) - 0, (ai_settings.screen_height/2) + 300)
        self.rect_border.center = ((ai_settings.screen_width/2) - 0, (ai_settings.screen_height/2) + 300)

        # The button message needs to be prepped ony once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = pygame.font.SysFont('monospace', 60).render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_border, self.rect_border)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets launched by the rocket ship."""

    def __init__(self, game_instance):
        """Initializes a bullet at rocket ship's position."""
        super().__init__()
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.color = self.settings.bullet_color

        # Creates a rectangular container for bullet at the right position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game_instance.ship.rect.midtop

        # Stores bullet's y-coordinate for speed manipulation
        self.y = float(self.rect.y)

    def update(self):
        """Moves the bullet up on screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draws a bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image and rotate to face left
        self.image = pygame.image.load("images/alien.bmp")
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()

        # Initial position (will be set by fleet)
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        """Move alien left across the screen."""
        self.rect.x -= self.settings.alien_speed

    def check_edges(self):
        """Return True if alien has reached the left edge of the screen."""
        return self.rect.left <= 0

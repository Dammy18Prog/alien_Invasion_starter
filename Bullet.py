import pygame
from pygame.sprite import Sprite
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired by the ship."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create bullet rect at the right side of ship
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midleft = ai_game.ship.rect.midright

        # Store float x position for smooth movement
        self.x = float(self.rect.x)

    def update(self):
        """Move bullet to the right."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw bullet on screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Bullet rectangle
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)

        # Start bullet at the RIGHT SIDE of the ship
        self.rect.midleft = ai_game.ship.rect.midright

        # Store float x-value for smooth movement
        self.x = float(self.rect.x)

    def update(self):
        # Move bullet horizontally to the right
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

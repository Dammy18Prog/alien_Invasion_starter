import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load and rotate ship to face right
        self.image = pygame.image.load("images/ship.bmp")
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()

        # Start on the left middle
        self.rect.midleft = self.screen_rect.midleft

        # Vertical position as float
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Move the ship up or down."""
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

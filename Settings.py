class Settings:
    """A class to store all game settings."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 15.0
        self.ships_limit = 3

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (255, 0, 0)

        # Alien settings
        self.alien_speed = 0.6
        self.alien_vertical_speed = 1.0

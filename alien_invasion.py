import sys
import pygame
from Settings_hw import Settings
from ship_hw import Ship
from bullet_hw import Bullet
from Alien_hw import Alien
from game_stats_hw import GameStats
from Scoreboard_hw import Scoreboard
from Button_hw import Button

class AlienInvasion:
    """Manage game assets and behavior."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion HW")

        # Game stats and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Play button
        self.play_button = Button(self, "Play")

        # Fleet vertical movement variables
        self.fleet_vertical_offset = 0
        self.fleet_vertical_direction = 1
        self.fleet_vertical_speed = 1

        # Create initial fleet
        self._create_fleet()

    def _create_fleet(self):
        """Create a fleet filling the screen top-to-bottom with space for horizontal movement."""
        self.aliens.empty()
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Margins
        left_margin = 250
        right_margin = 50

        # Vertical spacing
        available_space_y = self.settings.screen_height - 2 * alien_height
        number_rows = available_space_y // (alien_height + 20)  # 20px vertical spacing

        # Horizontal spacing
        available_space_x = self.settings.screen_width - left_margin - right_margin - alien_width
        number_cols = 4

        for col in range(number_cols):
            for row in range(number_rows):
                new_alien = Alien(self)
                new_alien.rect.x = self.settings.screen_width - right_margin - (col + 1) * (alien_width + 60)
                new_alien.rect.y = alien_height + row * (alien_height + 20)
                self.aliens.add(new_alien)

    def run_game(self):
        """Main loop."""
        clock = pygame.time.Clock()
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.ship.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.score = 0
            self.stats.level = 1
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self.fleet_vertical_offset = 0
            self.fleet_vertical_direction = 1
            self._create_fleet()
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        if len(self.bullets) < 5:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += 50 * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.stats.level += 1
            self.sb.prep_level()
            self.settings.alien_speed += 0.2
            self._create_fleet()

    def _update_aliens(self):
        """Update alien positions horizontally and vertically."""
        for alien in self.aliens.sprites():
            # Move left
            alien.rect.x -= self.settings.alien_speed
            # Move up/down
            alien.rect.y += self.fleet_vertical_speed * self.fleet_vertical_direction

        # Check if any alien reached top or bottom of screen
        top_edge = min(alien.rect.top for alien in self.aliens.sprites())
        bottom_edge = max(alien.rect.bottom for alien in self.aliens.sprites())
        
        if bottom_edge >= self.settings.screen_height or top_edge <= 0:
            self.fleet_vertical_direction *= -1  # Reverse vertical direction

        # Check collisions with ship
        for alien in self.aliens.sprites():
            if alien.rect.colliderect(self.ship.rect):
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.fleet_vertical_offset = 0
            self.fleet_vertical_direction = 1
            self._create_fleet()
            self.ship.rect.midleft = self.screen.get_rect().midleft
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()

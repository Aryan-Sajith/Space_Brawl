import sys
import pygame

from settings import Settings
from spaceship import SpaceShip
from bullet import Bullet
from alien import Alien


class SpaceBrawl:
    """Main class to manage Space Brawl's functionality."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.settings = Settings()

        # Setup main surface as full screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.main_width = self.screen.get_rect().width
        self.settings.main_height = self.screen.get_rect().height

        pygame.display.set_caption("Space Brawl")

        # Setup spaceship.
        self.ship = SpaceShip(self)

        # Setup bullets & aliens as a Sprite group
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create the fleet of aliens!
        self._create_fleet()

    def run_game(self):
        """The main game loop."""
        while True:
            self._manage_events()
            self.ship.move_continuously()
            self._update_bullets()
            self._update_screen()

    def _create_fleet(self):
        """Helper method within initializer to creates the fleet of aliens."""
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.main_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Create 1st row of aliens.
        for alien_number in range(number_aliens_x):
            self._create_alien(alien_number)

    def _create_alien(self, alien_number):
        """Helper of  _create_fleet() to create an alien and add it to the row."""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width * (1 + 2.3 * alien_number)
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _update_bullets(self):
        """Helper method for run_game() that updates bullets on screen and removes old ones"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            bullet: Bullet
            if bullet.bullet_rectangle.bottom <= 0:
                self.bullets.remove(bullet)

    def _manage_events(self):
        """Helper method of run_game() to manage user events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit condition.
                sys.exit()
            # Continuous movement
            elif event.type == pygame.KEYDOWN:
                self._manage_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._manage_keyup_events(event)

    def _manage_keydown_events(self, event):
        """Helper method of _manage_events() that responds to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # Another exit condition
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if len(self.bullets) < self.settings.bullets_limit:
                self._fire_bullet()

    def _fire_bullet(self):
        """Create a new bullet and add it to bullets group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """Helper method of run_game to update main surface and flip screen."""
        # Update main screen
        self.screen.fill(self.settings.background_color)

        # Draws rocket ship
        self.ship.blitme()

        # Draws bullets
        for bullet in self.bullets.sprites():
            bullet: Bullet
            bullet.draw_bullet()

        # Draws aliens
        self.aliens.draw(self.screen)

        # Display updated screen
        pygame.display.flip()

    def _manage_keyup_events(self, event):
        """Helper method of _manage_events() that responds to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


if __name__ == '__main__':
    # Runs the game.
    game = SpaceBrawl()
    game.run_game()
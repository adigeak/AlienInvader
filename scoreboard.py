import pygame.font
from pygame.sprite import Group
from ship import Ship
from pygame.transform import scale

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font setting for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_image()

    def prep_image(self):
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Make scoreboard"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "Score:{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        #display the score
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """make high score"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # display the score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 500
        self.high_score_rect.top = 20

    def prep_level(self):
        """make level """
        self.level_image = self.font.render(str(self.stats.level),True,
                                            self.text_color, self.ai_settings.bg_color)
        # positon
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            # ship.rect.width = 50
            # ship.rect.height = 50
            ship.image = scale(ship.image, (50,50))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 20 + ship_number * ship.rect.width *2
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        # Draw ships.
        self.ships.draw(self.screen)
import pygame

class Ship():
    """to descibe the feature of ship"""

    def __init__(self,all_set,screen):
        """Initalize the feature of ship and
        starting position"""
        self.screen = screen
        self.ai_settings = all_set

        # Load the ship image and get the rectangle.
        self.image = pygame.image.load('images/no_ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship' center.
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # Movement Flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Uptade the position of ship by the Key.up command"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        elif self.moving_up and self.rect.top > self.screen_rect.top:
            self.bottom -= self.ai_settings.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor

        # update rect object from self.center.
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        """Draw the ship at this location."""
        self.screen.blit(self.image,self.rect)
import pygame
from pygame.sprite import Sprite

class Background(Sprite):
    """A class for background image"""
    def __init__(self,ai_settings,location):
        super().__init__()
        self.image = pygame.image.load(ai_settings.bg_image)
        self.image = pygame.transform.scale(self.image,
                                            (ai_settings.screen_width,ai_settings.screen_height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

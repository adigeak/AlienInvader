import pygame
from setting import Setting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from background import Background
# from alien import Alien

def run_game():
    #Initiating everything
    pygame.init()
    all_set = Setting()
    screen = pygame.display.set_mode(
        (all_set.screen_width,all_set.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #load background image
    bg = Background(all_set,(0,0))

    # Make ship
    ship = Ship(all_set,screen)

    # Make the group to store bullets in.
    bullets = Group()

    # Make a group of aliens
    aliens = Group()

    # create the fleat of aliens.
    gf.create_fleet(all_set,screen,ship,aliens)

    #Begin the main part.
    while True:

        gf.checks_events(all_set,screen,ship,bullets)
        ship.update()
        gf.update_bullets(all_set,screen,ship,aliens,bullets)
        gf.update_aliens(all_set,ship,aliens)
        gf.update_screen(all_set,screen,ship,aliens,bullets,bg)

run_game()
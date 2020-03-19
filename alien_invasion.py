import pygame
from setting import Setting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from background import Background
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
# from alien import Alien

def run_game():
    #Initiating everything
    pygame.init()
    all_set = Setting()
    screen = pygame.display.set_mode(
        (all_set.screen_width, all_set.screen_height))

    # Make play Button.
    play_button = Button(all_set, screen, "Play")

    #Create an instance to store game statistics and create a scoreboard
    stats = GameStats(all_set)
    sb = Scoreboard(all_set, screen, stats)

    #load background image
    bg = Background(all_set,(0,0))

    # Make ship
    ship = Ship(all_set,screen)

    # Make the group to store bullets in.
    bullets = Group()

    # Make a group of aliens
    aliens = Group()

    # create the fleat of aliens.
    # gf.create_fleet(all_set,screen,ship,aliens)

    # load high_score
    gf.load_high_score(stats)

    #Begin the main part.
    while True:

        gf.checks_events(all_set,screen,ship,bullets,stats, play_button,aliens,sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(all_set,screen,ship,aliens,bullets,stats,sb)
            gf.update_aliens(all_set, stats, screen, bullets, ship, aliens,sb)
        # elif stats.ships_left <= 0:
        #     stats.reset_stats() # i have to make the play again button

        gf.update_screen(all_set,stats, screen,ship,aliens,bullets,bg,play_button,sb)

run_game()
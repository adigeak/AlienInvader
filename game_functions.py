import sys
from bullet import Bullet
from alien import Alien
import pygame
import json
from time import sleep

def save_high_score(stats):
    with open("data/score.json",'w') as f:
        json.dump(stats.high_score,f)

def load_high_score(stats):
    with open("data/score.json") as f:
        stats.high_score = json.load(f)

def checks_events(ai_settings,screen,ship,bullets,stats, play_button,aliens,sb):
    """Respond to keypress and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens,sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y,sb)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y,sb):
    """Start a new game when click play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets,sb)

def start_game(ai_settings, screen, stats, ship, aliens, bullets,sb):
    #reset the game settings
    ai_settings.initialize_dynamic_settings()
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Reset the sscoreboard image.
    sb.prep_image()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def create_fleet(ai_settings,screen,ship,aliens):
    """create a full fleat of aliens."""
    # create a alien
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x): # here we start from zero
            # because the top one will not be in the fleet that is used for calculation
            create_alien(ai_settings,screen,aliens,alien_number,row_number)


def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    """Create a alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien.rect.height + 2*alien.rect.height*row_number
    alien.rect.y = alien.y
    aliens.add(alien)

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return  number_aliens_x

def get_number_rows(ai_settings, ship_height,alien_height):
    """Determine the number of row of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height-
                         (3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens,sb):
    """Respond to Key Press"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_ESCAPE:
        save_high_score(stats)
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets,sb)
    else:
        pass

def check_keyup_events(event,ship):
    """Respond to key release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    else:
        pass

def fire_bullet(ai_settings,screen,ship,bullets):
    """fire a bullet if limit is not achived"""
    # Create a new bullet and add it to the bullet group.
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings,screen,ship,aliens,bullets,stats,sb):
    """update position of bullets and get rid of old bullets."""
    bullets.update()
    # check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    # get rid of old bullet as y continues to decrease.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    if len(aliens) == 0:
        # If the entire fleet is destroyed.
        # Destroy bullets and create a new fleet
        bullets.empty()
        ai_settings.increase_speed()
        # Increase Level
        stats.level += 1
        sb.prep_level()

        ship.center_ship()
        create_fleet(ai_settings,screen,ship,aliens)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships being hit by aliens.
        stats.ships_left -= 1

        # update score
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship.
        create_fleet(ai_settings,screen, ship, aliens)
        ship.center_ship()

        # pause.
        sleep(.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, screen, bullets, ship, aliens,sb):
    """Update the position of all aliens in the fleet."""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb)
        # print("ship hit!!!")
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb):
    """check weather the fleet reaches the bottomof the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_high_score(stats,sb):
    """check to see if there is new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_screen(ai_settings,stats, screen,ship,aliens,bullets,bg,play_button,sb):
    """Update Image on the screen and refresh the screen with flip"""
    # fill the background
    # screen.fill(ai_settings.bg_color)
    screen.blit(bg.image,bg.rect)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score info
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # making the screen visible to most recent one
    pygame.display.flip()
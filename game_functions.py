# Alien Invasion
# Created by: Hector Rodriguez & Justin Castillo
import sys
import time
import pygame, math, itertools
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button

def check_events(ai_settings, screen, stats, sb, quit_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, quit_button, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_main_event(ai_settings, screen, stats, sb, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_play_key(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_play_key(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Start a new game when the player presses any key."""
    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Start game
    ai_settings.home = False

def check_quit_button(ai_settings, screen, stats, sb, quit_button):
    """Start a new game when the player clicks Play."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_clicked = quit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.game_active:
        pygame.quit()

def check_keydown_events(event, ai_settings, screen, stats, sb, quit_button, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left.
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Fire bullets.
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        # Pause game.
        pause_game(ai_settings, screen, stats, sb, quit_button)

def pause_game(ai_settings, screen, stats, sb, quit_button):
    """Respond to 'p' to pause the game."""
    ai_settings.pause = True
    stats.game_active = True
    # Show the mouse cursor.
    pygame.mouse.set_visible(True)

    while ai_settings.pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ai_settings.pause = False
                    # Show the mouse cursor.
                    pygame.mouse.set_visible(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_high_score(stats, sb)
                check_quit_button(ai_settings, screen, stats, sb, quit_button)
        # Draw the score information, pause text and quit button on screen.
        quit_button.draw_button()
        sb.show_score()
        screen.blit(ai_settings.pause_text1, ((ai_settings.screen_width/2) - 110, (ai_settings.screen_height/2) - 180))
        screen.blit(ai_settings.pause_text2, ((ai_settings.screen_width/2) - 390, (ai_settings.screen_height/2) - 110))
        pygame.display.update()

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(ai_settings, screen, stats, sb, ship, aliens,bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets off screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            bullet.draw_explosion()

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update images on the screen and flip to the new screen."""
    # Draw the score information.
    sb.show_score()

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)

    # Make the most recently drawn screen visible.
    pygame.display.update()


def bg_update(ai_settings, screen, sb, y):
     # Redraw the screen during each pass through the loop.
    rel_y = y % ai_settings.bg.get_rect().height
    screen.blit(ai_settings.bg, (0, rel_y- ai_settings.bg.get_rect().height))
    if rel_y < ai_settings.screen_height:
        screen.blit(ai_settings.bg, (0, rel_y))
        # Draw the score information.
        sb.show_score()

def bg_main(ai_settings, screen, y_main):
     # Redraw the main screen during each pass through the loop.
    rel_y = y_main % ai_settings.bg.get_rect().height
    screen.blit(ai_settings.bg, (0, rel_y- ai_settings.bg.get_rect().height))
    if rel_y < ai_settings.screen_height:
        screen.blit(ai_settings.bg, (0, rel_y))

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the first fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width
    number_aliens_x = int(available_space_x / (1.4 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.3 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = ai_settings.screen_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge, and then update the 
        positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        stats.write_high_score_(stats.score)

def main_screen(ai_settings, screen):
    """Display main screen."""
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Title, credits, and version.
    screen.blit(ai_settings.title_text, ((ai_settings.screen_width/2) - 400, (ai_settings.screen_height/2) - 100))
    screen.blit(ai_settings.any_text, ((ai_settings.screen_width/2) - 200, (ai_settings.screen_height/2) + 100))
    screen.blit(ai_settings.version_text, (1500, 1030))
    screen.blit(ai_settings.version_credit, (50, 1030))
    screen.blit(ai_settings.version_hector, (150, 1030))
    screen.blit(ai_settings.version_jason, (200, 1030))
    pygame.display.flip()
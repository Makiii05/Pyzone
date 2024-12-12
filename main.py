import pygame
import hangman
import color_game
import rock_paper_scissors
import tic_tac_toe
import adventure

mainClock = pygame.time.Clock()
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.display.set_caption("PyZone")
screen = pygame.display.set_mode((1000, 550), 0, 32)
font = pygame.font.SysFont(None, 20)
click = False

def main():
    # Load and scale the background image
    background = pygame.image.load("assets/background.webp")
    background = pygame.transform.scale(background, (1000, 550))

    click = False
    while True:
        screen.blit(background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Define buttons
        hangmanButton = pygame.Rect(400, 275, 200, 35)
        TTTButton = pygame.Rect(400, 325, 200, 35)
        RPSButton = pygame.Rect(400, 375, 200, 35)
        ColorGameButton = pygame.Rect(400, 425, 200, 35)
        adventureButton = pygame.Rect(400, 475, 200, 35)

        # Button interactions
        if hangmanButton.collidepoint((mx, my)) and click:
            hangman.hangman()
        if TTTButton.collidepoint((mx, my)) and click:
            tic_tac_toe.tic_tac_toe()
        if RPSButton.collidepoint((mx, my)) and click:
            rock_paper_scissors.rock_paper_scissors()
        if ColorGameButton.collidepoint((mx, my)) and click:
            color_game.color_game()
        if adventureButton.collidepoint((mx, my)) and click:
            adventure.adventure()
        # Draw transparent rounded container
        butContainer = pygame.Rect(385, 260, 230, 265)
        container_surface = pygame.Surface((1000, 550), pygame.SRCALPHA)
        pygame.draw.rect(container_surface, (0, 0, 0, 192), butContainer, border_radius=20)
        screen.blit(container_surface, (0, 0))

        # Draw buttons
        pygame.draw.rect(screen, (255, 255, 255), hangmanButton, border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), TTTButton, border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), RPSButton, border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), ColorGameButton, border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), adventureButton, border_radius=20)

        # Render and center text in each button
        def draw_text_centered(text, button):
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)

        draw_text_centered("HANGMAN", hangmanButton)
        draw_text_centered("TIC - TAC - TOE", TTTButton)
        draw_text_centered("ROCK PAPER SCISSORS", RPSButton)
        draw_text_centered("COLOR GAME", ColorGameButton)
        draw_text_centered("ADVENTURE", adventureButton)

        click = False

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()
        mainClock.tick(60)

main()
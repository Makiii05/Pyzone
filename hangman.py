import pygame
import random
from english_words import get_english_words_set
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.display.set_caption("PyZone: Hangman")

# Screen setup
w, h = 1000, 550
screen = pygame.display.set_mode((w, h), 0, 32)
mainClock = pygame.time.Clock()

# Fonts
font_sm = pygame.font.SysFont(None, 20)
font = pygame.font.SysFont(None, 30)

# Globals
click = False

# -------------------- Helper Functions --------------------

def draw_text(text, font, color, surface, x, y):
    """Draws text on the given surface."""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def center_text(word, font):
    """Calculates the x position to center the given word on the screen."""
    get_word = font.render(word, True, (255, 255, 255))
    word_length = get_word.get_width()
    return (w / 2) - (word_length / 2)

def random_word():
    """Fetches a random word from the English word set."""
    words_set = get_english_words_set(['web2'])
    words_list = list(words_set)
    return random.choice(words_list).lower()

def print_answer_list(lst):
    """Formats the guessed word list for display."""
    return " ".join(lst)

def print_used_letters(lst):
    """Formats the guessed word list for display."""
    return " - ".join(lst)

def random_msg(var, letter):
    """Generates random feedback messages for correct/incorrect guesses."""
    random_phrases = {
        "correct": [
            "Way to go, champ!", "You’re on fire!", "Nailed it!",
            "Bingo! That’s right!", "You’re a genius!", "Bravo! Keep it up!"
        ],
        "incorrect": [
            "Not quite, try again.", "Close, but no cigar.", 
            "Oops! Better luck next time.", "Swing and a miss!"
        ]
    }
    stats = "" if var == "correct" else "not "
    return f"{random.choice(random_phrases[var])} {letter} is {stats}in the word!"

def hangman():
    """Runs the Hangman game with a life = 0 animation."""
    running = True
    rand_word = random_word()
    life = 6
    guessed_word = ["_" for _ in rand_word]
    used_letter = []
    message, message1 = "Press any letter...", ""
    stage = "assets/life_is_6.png"
    stageimage = pygame.image.load(stage)
    stageimage = pygame.transform.scale(stageimage, (250, 250))
    stage_rec = stageimage.get_rect(center=(w / 2, 260))

    # Animation setup for life = 0
    animation_dead = [
        f"assets/life_is_{i}.png" for i in range(7, 0, -1)
    ]  # Replace with actual animation frames
    animation_jump = [
        f"assets/jump_{i}.png" for i in range(1, 3)
    ]  # Replace with actual animation frames
    animation_index = 0
    animation_timer = 0  # Time tracker for animation frames
    animation_interval = 200  # Milliseconds (1 second per frame)

    while running:
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

        # Check win or loss condition
        if "".join(guessed_word) == rand_word.upper():
            message = "You guessed the word! Good job! Try Again?"
            message1 = "Press [spacebar] to continue or [esc] to exit."
            # Handle animation
            if current_time - animation_timer > animation_interval:
                animation_timer = current_time
                animation_index = (animation_index + 1) % len(animation_jump)
                stageimage = pygame.image.load(animation_jump[animation_index])
                stageimage = pygame.transform.scale(stageimage, (250, 250))
        elif life == 0:
            message = f"Oh no! You ran out of lives. The word was {rand_word.upper()}!"
            message1 = "Press [spacebar] to continue or [esc] to exit."
            # Handle animation
            if current_time - animation_timer > animation_interval:
                animation_timer = current_time
                animation_index = (animation_index + 1) % len(animation_dead)
                stageimage = pygame.image.load(animation_dead[animation_index])
                stageimage = pygame.transform.scale(stageimage, (250, 250))

        # Draw elements
        screen.blit(stageimage, stage_rec)
        draw_text("WELCOME TO HANGMAN!", font, (255, 255, 255), screen, center_text("WELCOME TO HANGMAN!", font), 50)
        draw_text(f"Life: {life}", font, (255, 255, 255), screen, center_text(f"Life: {life}", font), 90)
        draw_text(print_answer_list(guessed_word), font, (255, 255, 255), screen, center_text(print_answer_list(guessed_word), font), 410)
        draw_text(message, font_sm, (255, 255, 255), screen, center_text(message, font_sm), 450)
        draw_text(message1, font_sm, (255, 255, 255), screen, center_text(message1, font_sm), 480)
        draw_text(f"Used Letter: {print_used_letters(used_letter)}", font, (255, 255, 255), screen, center_text(f"Used Letters: {used_letter}", font), 500)


        # Back button
        mx, my = pygame.mouse.get_pos()
        backBtn = pygame.Rect(20, 20, 100, 35)
        pygame.draw.rect(screen, (255, 255, 255), backBtn, border_radius=20)
        back_text = font_sm.render("BACK", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=backBtn.center)
        screen.blit(back_text, back_text_rect)

        # Button click logic
        if backBtn.collidepoint((mx, my)) and click:
            running = False

        # Event handling
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if life == 0 or "".join(guessed_word) == rand_word.upper():
                    if event.key == K_SPACE:
                        rand_word = random_word()
                        life = 6
                        guessed_word = ["_" for _ in rand_word]
                        used_letter = []
                        message, message1 = "Press any letter...", ""
                        animation_index = 0
                        stageimage = pygame.image.load("assets/life_is_6.png")
                        stageimage = pygame.transform.scale(stageimage, (250, 250))
                elif pygame.K_a <= event.key <= pygame.K_z and life > 0:
                    letter = chr(event.key).upper()
                    used_letter.append(letter)
                    if letter in rand_word.upper():
                        for i in range(len(rand_word)):
                            if letter == rand_word[i].upper():
                                guessed_word[i] = letter
                        message = random_msg("correct", letter)
                    else:
                        life -= 1
                        message = random_msg("incorrect", letter)
                        if life > 0:
                            stage = f"assets/life_is_{life}.png"
                            stageimage = pygame.image.load(stage)
                            stageimage = pygame.transform.scale(stageimage, (250, 250))
                    
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()
        mainClock.tick(60)

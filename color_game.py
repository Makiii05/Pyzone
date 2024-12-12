import pygame
import random
import time
from english_words import get_english_words_set
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.display.set_caption("PyZone: Color Game")

# Screen setup
w, h = 1000, 550
screen = pygame.display.set_mode((w, h), 0, 32)
mainClock = pygame.time.Clock()

# Fonts
font_lg = pygame.font.SysFont(None, 40)
font_sm = pygame.font.SysFont(None, 20)
font = pygame.font.SysFont(None, 30)

# Globals
    
# ------------------ Helper Functions --------------------

def draw_text(text, font, color, surface, x, y):
    """Draws text on the given surface."""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
def draw_text_btn(text, color, btn, font_size, border_color, border_thickness):
    # Render the text with the font
    text_surface = font_size.render(f"{text}", True, color)
    text_rect = text_surface.get_rect(center=btn.center)

    # Render the border
    for x_offset in range(-border_thickness, border_thickness + 1):
        for y_offset in range(-border_thickness, border_thickness + 1):
            if x_offset == 0 and y_offset == 0:
                continue  # Skip the center (original text position)
            border_surface = font_size.render(f"{text}", True, border_color)
            border_rect = text_rect.copy()
            border_rect.move_ip(x_offset, y_offset)
            screen.blit(border_surface, border_rect)

    # Render the main text
    screen.blit(text_surface, text_rect)
def random_color():
    colors = {
        "redBtn": (255, 0, 0),
        "whiteBtn": (255, 255, 255),
        "pinkBtn": (255, 192, 203),
        "yellowBtn": (255, 255, 0),
        "blueBtn": (0, 0, 255),
        "greenBtn": (0, 255, 0)
    }

    return random.choice(list(colors.keys()))
def center_text(word, font):
    """Calculates the x position to center the given word on the screen."""
    get_word = font.render(word, True, (255, 255, 255))
    word_length = get_word.get_width()
    return (w / 2) - (word_length / 2)

def color_game():
    running = True
    rolling = False
    click = False
    amount = 5
    totalMoney = 100
    latest = {
        "c0" : [(255,0,0), 0,'null'],
        "c1" : [(0,0,255), 0,'null'],
        "c2" : [(0,255,0), 0,'null']
    }
    colors = {
        "redBtn": (255, 0, 0),
        "whiteBtn": (255, 255, 255),
        "pinkBtn": (255, 192, 203),
        "yellowBtn": (255, 255, 0),
        "blueBtn": (0, 0, 255),
        "greenBtn": (0, 255, 0)
    }
    background = pygame.image.load("assets/color_game_bg.png")
    background = pygame.transform.scale(background, (1000, 550))
    button_surface = pygame.Surface((75, 75), pygame.SRCALPHA)
    rolled_surface = button_surface
    CFrame = "assets/color_frame/1.png"
    CFrameimage = pygame.image.load(CFrame)
    CFrameimage1 = pygame.transform.scale(CFrameimage, (225, 225))
    CFrame_rec1 = CFrameimage1.get_rect(center=(225, 200))
    CFrameimage2 = pygame.transform.scale(CFrameimage, (225, 225))
    CFrame_rec2 = CFrameimage2.get_rect(center=(425, 200))
    CFrameimage3 = pygame.transform.scale(CFrameimage, (225, 225))
    CFrame_rec3 = CFrameimage3.get_rect(center=(625, 200))

    # Animation setup for life = 0
    roll_animation = [
        f"assets/color_frame/{i}.png" for i in range(1, 41)
    ]  # Replace with actual animation frames
    r_roll_animation = [
        f"assets/color_frame/{i}.png" for i in range(41, 0, -1)
        ]  # Replace with actual animation frames
    animation_index = 0
    animation_timer = 0  # Time tracker for animation frames
    animation_interval = 20  # Milliseconds (1000 = 1 second per frame)
        
    bets_btn = {
        "redBtn": [pygame.Rect(343, 368, 75, 75), 0],
        "whiteBtn": [pygame.Rect(143, 368, 75, 75), 0],
        "pinkBtn": [pygame.Rect(243, 368, 75, 75), 0],
        "yellowBtn": [pygame.Rect(640, 368, 75, 75), 0],
        "blueBtn": [pygame.Rect(442, 368, 75, 75), 0],
        "greenBtn": [pygame.Rect(541, 368, 75, 75), 0]
    }

    def plus_bet(color, amount):
        """Increase the bet for a specific color."""
        bets_btn[color][1] += amount
        return amount

    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

        mx, my = pygame.mouse.get_pos()

        # Buttons
        backBtn = pygame.Rect(20, 20, 100, 35)
        
        rolled_color0 = pygame.Rect(140, 105, 170, 170)
        rolled_color1 = pygame.Rect(340, 105, 170, 170)
        rolled_color2 = pygame.Rect(540, 105, 170, 170)

        color0 = pygame.Rect(778, 320, 40, 40)
        color1 = pygame.Rect(778, 365, 40, 40)
        color2 = pygame.Rect(778, 410, 40, 40)
        won0 = pygame.Rect(838, 320, 40, 40)
        won1 = pygame.Rect(838, 365, 40, 40)
        won2 = pygame.Rect(838, 410, 40, 40)

        rollsCon = pygame.Rect(778, 285, 140, 30)
        totalCon = pygame.Rect(778, 72, 140, 30)
        rollBtn = pygame.Rect(778, 218, 140, 30)
        amtCon = pygame.Rect(778, 142, 80, 30)
        addBetBtn = pygame.Rect(858, 142, 30, 30)
        minusBetBtn = pygame.Rect(888, 142, 30, 30)

        # Check interactions
        if backBtn.collidepoint((mx, my)) and click:
            running = False
        if amount <= totalMoney > 0:
            for key, value in bets_btn.items():
                if value[0].collidepoint((mx, my)) and click:
                    totalMoney -= plus_bet(f"{key}", amount)
        if any(value != 0 for _, value in bets_btn.values()):  # Check if any bet is non-zero
            if rollBtn.collidepoint((mx, my)) and click:
                if rolling == False:
                    rolling = True
                    rolled_surface = button_surface
                else:
                    rolling = False
                    rolled_surface = screen
                    current_color = [random_color(),random_color(),random_color()]
                    for key in bets_btn.keys():
                        bet_num = bets_btn[key][1]
                        if bet_num != 0 and key in current_color:
                            bets_btn[key][1] += (bets_btn[key][1] * current_color.count(key))
                            totalMoney += bets_btn[key][1]
                            i = current_color.index(key)
                            latest[f"c{i}"][1] = bets_btn[key][1]
                            latest[f"c{i}"][2] = current_color[i]
                        else:
                            bets_btn[key][1] = 0
                    for i in range(len(current_color)):
                        latest[f"c{i}"][0] = colors[current_color[i]]
                        if latest[f"c{i}"][2] not in current_color:
                            latest[f"c{i}"][1] = 0
                            latest[f"c{i}"][2] = "null"
                            

                    for key in bets_btn.keys():
                        bets_btn[key][1] = 0

            
        if rolling == True:
            if current_time - animation_timer > animation_interval:
                animation_timer = current_time
                animation_index = (animation_index + 1) % len(roll_animation)
                CFrameimage1 = pygame.image.load(roll_animation[animation_index])
                CFrameimage1 = pygame.transform.scale(CFrameimage1, (225, 200))
                CFrameimage2 = pygame.image.load(r_roll_animation[animation_index])
                CFrameimage2 = pygame.transform.scale(CFrameimage2, (225, 200))
                CFrameimage3 = pygame.image.load(roll_animation[animation_index])
                CFrameimage3 = pygame.transform.scale(CFrameimage3, (225, 200))


        if addBetBtn.collidepoint((mx, my)) and click:
            if amount < totalMoney:
                amount += 5
        if minusBetBtn.collidepoint((mx, my)) and click:
            if amount > 0:
                amount -= 5

        # Draw buttons and bets
        screen.blit(CFrameimage1, CFrame_rec1)
        screen.blit(CFrameimage2, CFrame_rec2)
        screen.blit(CFrameimage3, CFrame_rec3)


        pygame.draw.rect(screen, (255, 255, 255), backBtn, border_radius=20)

        pygame.draw.rect(rolled_surface, (210, 180, 140), rolled_color0)
        inner_rect0 = rolled_color0.inflate(-2* 10, -2*10)
        pygame.draw.rect(rolled_surface, latest["c0"][0], inner_rect0)
        
        pygame.draw.rect(rolled_surface, (210, 180, 140), rolled_color1)
        inner_rect1 = rolled_color1.inflate(-2* 10, -2*10)
        pygame.draw.rect(rolled_surface, latest["c1"][0], inner_rect1)
        
        pygame.draw.rect(rolled_surface, (210, 180, 140), rolled_color2)
        inner_rect2 = rolled_color2.inflate(-2* 10, -2*10)
        pygame.draw.rect(rolled_surface, latest["c2"][0], inner_rect2)

        pygame.draw.rect(screen, latest["c0"][0], color0)
        pygame.draw.rect(screen, latest["c1"][0], color1)
        pygame.draw.rect(screen, latest["c2"][0], color2)

        pygame.draw.rect(button_surface, (0, 0, 0), won0)      # amount con
        pygame.draw.rect(button_surface, (0, 0, 0), won1)      # amount con
        pygame.draw.rect(button_surface, (0, 0, 0), won2)      # amount con
        pygame.draw.rect(button_surface, (0, 0, 0), rollsCon)      # amount con
        pygame.draw.rect(button_surface, (0, 0, 0), totalCon)      # amount con
        pygame.draw.rect(button_surface, (0, 0, 0), amtCon)      # amount con
        pygame.draw.rect(button_surface, (0, 0, 0), addBetBtn)      # add button
        pygame.draw.rect(button_surface, (0, 0, 0), minusBetBtn)      # minus button
        pygame.draw.rect(button_surface, (0, 0, 0), rollBtn)      # amount con

        # Draw "BACK" text
        draw_text_btn("BACK", (0, 0, 0), backBtn, font_sm, (255, 255, 255), 2)
        draw_text_btn(f"{amount}", (255, 255, 255), amtCon, font, (0, 0, 0), 1)
        draw_text_btn(f"{totalMoney}", (255, 255, 255), totalCon, font, (0, 0, 0), 1)
        draw_text_btn(f"Roll / Stop", (255, 255, 255), rollBtn, font, (0, 0, 0), 1)
        draw_text_btn(f"Last Roll", (255, 255, 255), rollsCon, font, (0, 0, 0), 1)
        draw_text_btn(f"P {latest['c0'][1]}", (255, 255, 255), won0, font, (0, 0, 0), 1)
        draw_text_btn(f"P {latest['c1'][1]}", (255, 255, 255), won1, font, (0, 0, 0), 1)
        draw_text_btn(f"P {latest['c2'][1]}", (255, 255, 255), won2, font, (0, 0, 0), 1)

        # Draw bet amounts
        for color,rect in bets_btn.items():
            pygame.draw.rect(button_surface, (255, 0, 0), rect[0])      # Red button
            draw_text_btn(f"{"" if(bets_btn[color][1] == 0)else bets_btn[color][1]}", (255,255,255), rect[0], font, (0, 0, 0), 1)

        # Handle events
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
        if totalMoney == 0 and bets_btn["redBtn"][1] == 0 and bets_btn["whiteBtn"][1] == 0  and bets_btn["pinkBtn"][1] == 0 and bets_btn["yellowBtn"][1] == 0  and bets_btn["blueBtn"][1] == 0 and bets_btn["greenBtn"][1] == 0:
            amount = 0

            con = pygame.Rect(325, 175, 350,200)
            exitBtn = pygame.Rect(370, 298, 120,35)
            retryBtn = pygame.Rect(520, 298, 120,35)
            
            if exitBtn.collidepoint((mx, my)) and click:
                running = False
            if retryBtn.collidepoint((mx, my)) and click:
                running = False
                color_game()
            
            pygame.draw.rect(screen, (192, 192, 192), con, border_radius=20)
            pygame.draw.rect(screen, (255, 0, 0), exitBtn, border_radius=10)
            pygame.draw.rect(screen, (0, 255, 0), retryBtn, border_radius=10)

            draw_text("Game Over!", font_lg, (0,0,0), screen, center_text("Game Over!", font_lg), 218)
            draw_text("try again?", font_sm, (0,0,0), screen, center_text("try again?", font_sm), 248)
            draw_text_btn(f"Exit", (255, 255, 255), exitBtn, font, (0, 0, 0), 1)
            draw_text_btn(f"Retry", (255, 255, 255), retryBtn, font, (0, 0, 0), 1)


        pygame.display.update()
        mainClock.tick(60)
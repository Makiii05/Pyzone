import pygame

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("PyZone")
screen = pygame.display.set_mode((1000,550),0,32)
font = pygame.font.SysFont(None, 20)
click = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
def rock_paper_scissors():
    running = True
    while running:
        screen.fill((0,0,0))
                
        mx, my = pygame.mouse.get_pos()
        backBtn = pygame.Rect(20, 20, 100, 35)
        if backBtn.collidepoint((mx, my)) and click:
            running = False
        pygame.draw.rect(screen, (255, 255, 255), backBtn, border_radius=20)
        
        # Draw "BACK" text centered on the button
        back_text = font.render("BACK", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=backBtn.center)
        screen.blit(back_text, back_text_rect)
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
        
        pygame.display.update()
        mainClock.tick(60)

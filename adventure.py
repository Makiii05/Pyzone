import pygame, sys
from pytmx.util_pygame import load_pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((16, 16))  # Player size
        self.image.fill((255, 0, 0))  # Red color for the player
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def update(self, keys, tangible_tiles):
        # Apply gravity
        self.velocity.y += 0.75  # Simulates gravity
        if self.velocity.y > 60:  # Limit fall speed
            self.velocity.y = 10

        # Handle movement
        if keys[K_LEFT] or keys[K_a]:
            self.velocity.x = -4
        elif keys[K_RIGHT] or keys[K_d]:
            self.velocity.x = 4
        else:
            self.velocity.x = 0

        # Jumping
        if self.on_ground:
            self.velocity.y = -14  # Jump power

        # Update position and handle collisions
        self.rect.x += self.velocity.x
        self.collide(tangible_tiles, "x")
        self.rect.y += self.velocity.y
        self.on_ground = False  # Reset on_ground before checking collisions
        self.collide(tangible_tiles, "y")

    def collide(self, tiles, direction):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if direction == "x":
                    # Prevent horizontal teleportation when inside a tile
                    if self.velocity.y >= 0 and self.rect.bottom > tile.rect.top:
                        # If falling or on ground, check if mostly inside tile vertically
                        if self.velocity.x > 0:  # Moving right
                            self.rect.right = tile.rect.left
                        elif self.velocity.x < 0:  # Moving left
                            self.rect.left = tile.rect.right
                        self.velocity.x = 0
                elif direction == "y":
                    if self.velocity.y > 0:  # Falling
                        # Only collide if player is above the tile
                        if self.rect.bottom > tile.rect.top and self.rect.top < tile.rect.top:
                            self.rect.bottom = tile.rect.top
                            self.on_ground = True  # Player is on the ground
                            self.velocity.y = 0
                    elif self.velocity.y < 0:  # Moving upward (jumping)
                        # Pass through when jumping up
                        pass
class Camera:
    def __init__(self, width, height):
        self.offset = pygame.math.Vector2(0, 0)  # Offset for camera movement
        self.width = width
        self.height = height

    def apply(self, entity):
        # Adjust the entity's position by the camera offset
        return entity.rect.topleft - self.offset

    def update(self, target):
        # Center the camera on the target (player)
        self.offset.y = target.rect.centery - self.height // 2
        self.offset.x = target.rect.centerx - self.width // 2

def adventure():
    mainClock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("PyZone")
    screen_width, screen_height = 1000, 550
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    tmx_data = load_pygame('terrain/level/Jumper2.tmx')
    sprite_group = pygame.sprite.Group()
    tangible_tiles = pygame.sprite.Group()
    SCALE = 2  # Adjust this scale factor as needed

    # Camera setup
    camera = Camera(screen_width, screen_height)

    # Load tiles
    for layer in tmx_data.visible_layers:
        for x, y, surf in layer.tiles():
            pos = (x * 16 * SCALE, y * 16 * SCALE)
            scaled_surf = pygame.transform.scale(
                surf, (surf.get_width() * SCALE, surf.get_height() * SCALE)
            )
            if layer.name == "tangible":
                Tile(pos=pos, surf=scaled_surf, groups=[sprite_group, tangible_tiles])
            else:
                Tile(pos=pos, surf=scaled_surf, groups=sprite_group)

    # Create player
    player = Player(pos=(550, 900), groups=sprite_group)

    font = pygame.font.SysFont(None, 20)
    click = False
    running = True

    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        keys = pygame.key.get_pressed()

        mx, my = pygame.mouse.get_pos()
        backBtn = pygame.Rect(20, 20, 100, 35)  # Define the button rectangle

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if backBtn.collidepoint((mx, my)):
                    running = False

        # Update the player and camera
        player.update(keys, tangible_tiles)
        camera.update(player)

        # Draw the tiles and player relative to the camera offset
        for sprite in sprite_group:
            screen.blit(sprite.image, camera.apply(sprite))

        # Draw the back button on top of everything
        pygame.draw.rect(screen, (255, 255, 255), backBtn, border_radius=20)
        back_text = font.render("BACK", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=backBtn.center)
        screen.blit(back_text, back_text_rect)

        pygame.display.update()
        mainClock.tick(60)
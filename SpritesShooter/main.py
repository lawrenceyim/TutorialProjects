import pygame
import sys
import random

# class Crosshair(pygame.sprite.Sprite):
#     def __init__(self, width, height, position_x, position_y, color):
#         super().__init__()
#         self.image = pygame.Surface([width, height])
#         self.image.fill(color)
#         self.rect = self.image.get_rect()
#         self.rect.center = [position_x, position_y]


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("gunshot.mp3")

    def shoot(self):
        self.gunshot.play()
        pygame.sprite.spritecollide(crosshair, target_group, True)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, position_x, position_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [position_x, position_y]


# General setup
pygame.init()
clock = pygame.time.Clock()

# Game screen
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("BG.png")
pygame.mouse.set_visible(False)

# Crosshair
crosshair = Crosshair("crosshair.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Target
target_group = pygame.sprite.Group()
for target in range(20):
    new_target = Target("target.png", random.randrange(0, screen_width), random.randrange(0, screen_height))
    target_group.add(new_target)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()

    pygame.display.flip()

    # Display background with nested loop since background image is only 256 * 256 px
    for y in range(0, screen_height, 256):
        for x in range(0, screen_width, 256):
            screen.blit(background, (x, y))

    # Order of draw matters because the draw functions called later will show in front of other draw objects
    # draw(screen) tells target_group to draw on screen
    target_group.draw(screen)

    # draw(screen) tells crosshair_group to draw on screen
    crosshair_group.draw(screen)
    crosshair_group.update()

    # Per second, at most 60 frames should pass
    clock.tick(60)
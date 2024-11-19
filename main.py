import pygame

pygame.init()

class Game:
    def __init__(self, screen_width, screen_height, money, score, bee_background_image, screen):
        self.screen_width = 1440
        self.screen_height = 864
        self.money = 0
        self.score = 0
        self.bee_background_image = pygame.image.load("images/title_screen_bee.png")

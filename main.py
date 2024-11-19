import pygame

pygame.init()

class Game:
    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 864
        self.money = 0
        self.score = 0
        self.background_color_image = 0 #add thissss
        self.bee_background_image = pygame.image.load("images/title_screen_bee.png")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def display_menu():
        pygame.blit


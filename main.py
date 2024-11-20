import pygame

pygame.init()

class Game:
    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 864
        self.money = 0
        self.score = 0
        self.background_color_image = pygame.image.load("images/grass_background.png")
        self.bee_background_image = pygame.image.load("images/title_screen_bee.png")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def display_menu(self):
        self.screen.blit(self.background_color_image, (0,0))
        self.screen.blit(self.bee_background_image, (0,0))
        pygame.display.update()
        


class Button:
    def __init__(self, inactive_color, active_color, text, position, width, height, action):
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.action = action

    def draw_button(self):
        

NewGame = Game()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display the menu
    NewGame.display_menu()
    
pygame.quit()


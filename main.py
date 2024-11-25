import pygame
pygame.init()


# Colour constants
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)

class Game:
    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 864
        self.money = 0
        self.score = 0
        self.background_color_image = pygame.image.load("images/grass_background.png")
        self.bee_background_image = pygame.image.load("images/title_screen_bee.png")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Display the menu
            NewGame.display_menu()

    def display_menu(self):
        self.screen.blit(self.background_color_image, (0,0))
        self.screen.blit(self.bee_background_image, (0,0))

        # Create and display start button
        StartButton = Button(GREEN, LIGHT_GREEN, "Start", (216, 550), 450, 100, self.start_game)
        StartButton.draw_button(self.screen)

        # Create and display quit button
        QuitButton = Button(RED, LIGHT_RED, "Quit", (774, 550), 450, 100, self.quit)
        QuitButton.draw_button(self.screen)

    
        pygame.display.update()
        
    def start_game(self):
        pass

    def quit(self):
        self.running = False
        pygame.quit()


class Button:
    def __init__(self, inactive_color, active_color, text, position, width, height, action=None):
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.action = action

    def draw_button(self, screen):
        pygame.draw.rect(screen, self.inactive_color, (self.position[0], self.position[1], self.width, self.height))


    def is_hovered(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

NewGame = Game()



NewGame.run()

    
pygame.quit()


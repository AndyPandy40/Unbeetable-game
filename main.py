import pygame
pygame.init()


# Colour constants
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def display_text(text, position, size, color, screen):
    font = pygame.font.Font("freesansbold.ttf", size)
    text = font.render(text, True, color)

    text_rect = text.get_rect(center=(position))

    screen.blit(text, text_rect)




class Game:
    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 864
        self.money = 0
        self.score = 0

        self.background_color_image = pygame.image.load("images/grass_background.png")
        self.bee_background_image = pygame.image.load("images/title_screen_bee.png")

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.run_start_screen = True
        self.run_game = False
        self.clock = pygame.time.Clock()


        self.start_button = Button(GREEN, LIGHT_GREEN, "Start", (216, 550), 450, 100, self.display_game)
        self.quit_button = Button(RED, LIGHT_RED, "Quit", (774, 550), 450, 100, self.quit)

        self.screen.blit(self.background_color_image, (0,0))
        self.screen.blit(self.bee_background_image, (0,0))

    def run(self):
        while self.run_start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            # Display the menu
            self.display_menu()
            self.clock.tick(120)
            print(self.clock.get_fps())

        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            # Display the game
            self.display_game()
            self.clock.tick(120)
            print(self.clock.get_fps())

    def display_menu(self):
        # Create and display start button
        self.start_button.draw_button(self.screen)

        # Create and display quit button
        self.quit_button.draw_button(self.screen)

        display_text("Unbeetable Game",(720, 100), 130, BLACK, self.screen)
        display_text("Unbeetable Game",(717, 100), 130, LIGHT_GREEN, self.screen)
        pygame.display.update()
        
    def display_game(self):
        self.screen.fill(WHITE)
        self.run_start_screen = False
        self.run_game = True

        pygame.display.update()


    def quit(self):
        self.run_start_screen = False
        pygame.quit()
        exit()


class Button:
    def __init__(self, inactive_color, active_color, text, position, width, height, action=None):
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.action = action

        self.button_center = ((self.position[0] + (self.width//2)), self.position[1] + (self.height//2))
    def draw_button(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()



        # check if user is hovering over button
        if self.position[0] < mouse[0] < self.position[0] + self.width and self.position[1] < mouse[1] < self.position[1] + self.height:
            button_color = self.active_color
            if click[0]:
                self.action()
        else:
            button_color = self.inactive_color

        pygame.draw.rect(screen, button_color, (self.position[0], self.position[1], self.width, self.height))

        
        
        # Display text on button
        display_text(self.text, self.button_center, 60, BLACK, screen)





NewGame = Game()



NewGame.run()

    
pygame.quit()
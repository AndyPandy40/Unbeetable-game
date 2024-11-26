import pygame
pygame.init()


# Colour constants
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 864
        self.money = 0
        self.score = 0
        self.frame = 0
        self.background_color_image = pygame.image.load("images/grass_background.png")
        self.bee_background_image = pygame.image.load("images/title_screen_bee.png")

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.clock = pygame.time.Clock()


        self.start_button = Button(GREEN, LIGHT_GREEN, "Start", (216, 550), 450, 100, self.start_game)
        self.quit_button = Button(RED, LIGHT_RED, "Quit", (774, 550), 450, 100, self.quit)

        self.screen.blit(self.background_color_image, (0,0))
        self.screen.blit(self.bee_background_image, (0,0))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Display the menu
            NewGame.display_menu()
            self.clock.tick(200)
            print(self.clock.get_fps())

    def display_menu(self):
        



        # Create and display start button
        self.start_button.draw_button(self.screen)

        # Create and display quit button
        self.quit_button.draw_button(self.screen)

        self.frame += 1
    
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
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()



        # check if user is hovering over button
        if self.position[0] < mouse[0] < self.position[0] + self.width and self.position[1] < mouse[1] < self.position[1] + self.height:
            button_color = self.active_color
        else:
            button_color = self.inactive_color

        pygame.draw.rect(screen, button_color, (self.position[0], self.position[1], self.width, self.height))
        
        # Display text on button
        font = pygame.font.Font("freesansbold.ttf", 60)
        text = font.render(self.text, True, BLACK)

        button_center = ((self.position[0] + (self.width//2)), self.position[1] + (self.height//2))
        text_rect = text.get_rect(center=(button_center))
        
        screen.blit(text, text_rect)




NewGame = Game()



NewGame.run()

    
pygame.quit()
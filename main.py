import pygame
pygame.init()


# Colour constants
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Function to make displaying text easier
def display_text(text, position, size, color, screen):
    font = pygame.font.Font("freesansbold.ttf", size)
    text = font.render(text, True, color)

    text_rect = text.get_rect(center=(position))

    screen.blit(text, text_rect)




class GameStartScreen:
    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 864


        # Loads the background images
        self.background_color_image = pygame.image.load("images/grass_background.png")
        self.bee_background_image = pygame.image.load("images/title_screen_bee.png")
        self.title_text = pygame.image.load("images/Unbeetable_game_text.png")

        self.screen = pygame.display.set_mode((self.screen_width, 960))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.run_start_screen = True
        self.run_game = False
        self.clock = pygame.time.Clock()

        self.frame = 0
        
        # Displays background images and text
        self.screen.blit(self.background_color_image, (0,0))
        self.screen.blit(self.bee_background_image, (0,0))
        self.screen.blit(self.title_text, (80,20))


        # Displays buttons at start of code
        self.start_button = Button(GREEN, LIGHT_GREEN, "Start", (216, 550), 450, 100, self.display_game)
        self.quit_button = Button(RED, LIGHT_RED, "Quit", (774, 550), 450, 100, self.quit)



    def run(self):
        while self.run_start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            # Display the menu
            self.display_menu()
            self.clock.tick(120)
            #print(self.clock.get_fps())




    def display_menu(self):
        #print("displaying menu")
        # Create and display start button
        self.start_button.draw_button(self.screen)

        # Create and display quit button
        self.quit_button.draw_button(self.screen)

        pygame.display.update()
        

    def display_game(self):
        Game = MainGame(self.screen)
        self.run_start_screen = False
        Game.run_game()


    def quit(self):
        self.run_start_screen = False
        pygame.quit()
        exit()


class MainGame:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = 1440
        self.clock = pygame.time.Clock()

        self.screen_height = 960
        self.screen.fill(WHITE)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        NewMap = Map()
        NewMap.draw_tilemap(self.screen)
        self.Bee = Bees(16, BLACK, 100, 100, True, (100,100))
        

    def run_game(self):
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()


            self.Bee.animate_bee((100, 100), self.screen)
            # Display the game
            #self.display_game()
            self.clock.tick(120)
            #print(self.clock.get_fps())

            pygame.display.update()

    def display_game(self):
        pass

    def quit(self):
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


        # Check if user is hovering over button
        if self.position[0] < mouse[0] < self.position[0] + self.width and self.position[1] < mouse[1] < self.position[1] + self.height:
            button_color = self.active_color
            if click[0]:
                self.action()
        else:
            button_color = self.inactive_color

        pygame.draw.rect(screen, button_color, (self.position[0], self.position[1], self.width, self.height))

        
        
        # Display text on button
        display_text(self.text, self.button_center, 60, BLACK, screen)


class Map:
    def __init__(self):
        self.tile_size = 96

        self.grass_img = pygame.image.load("images/tiles/grass.png")
        self.grass_img = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
 
        self.path_img = pygame.image.load("images/tiles/path.png")
        self.path_img = pygame.transform.scale(self.path_img, (self.tile_size, self.tile_size))

        self.tilemap = [ 
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
            [0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0], 
            [0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0], 
            [1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0], 
            [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1], 
            [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1], 
            [1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0], 
            [0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0], 
            [0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]

        self.tile_images = {
            0: self.grass_img,
            1: self.path_img,
        }


    def draw_tilemap(self, screen):
            # Iterates through each element in the 2d array
            for row in range(len(self.tilemap)):
                for col in range(len(self.tilemap[row])):
                    tile_type = self.tilemap[row][col] # Finds the tile type at a position (1 or 0)
                    tile_image = self.tile_images[tile_type] # Matches it with the image using the dictionary
                    screen.blit(tile_image, (col * self.tile_size, row * self.tile_size)) # Displays them in order using their position in the array and size


class Bees:
    def __init__(self, size, color, health, speed, exists: bool, position):
        self.sprite_sheet = pygame.image.load("images/bees/bee.png")
        self.size = size
        self.color = color
        self.health = health
        self.speed = speed
        self.exists = exists
        self.position = position
        self.animation_frame = 0
        self.animation_list = []
        self.animation_steps = 6
        self.animation_cooldown = 100

        # Loop through the sprite sheet
        for x in range(self.animation_steps):
            # Get the inividual frames for the bee and append them to an array
            self.animation_list.append(self.get_image(x, self.size, self.size))
            print("frame", x, "appended to list")


    def get_image(self, level, width, height):

        # Create a surface to blit the image onto
        image = pygame.Surface((width, height))

        # Blit the frame of the bee onto the surface
        image.blit(self.sprite_sheet, (0,0), ((level*width, 0, width, height)))

        # Make the background transparent
        image.set_colorkey(self.color)

        return image
    
    def animate_bee(self, position, screen):
        last_update = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= self.animation_cooldown:

            print(current_time)
            print(last_update)
            last_update = current_time
            self.animation_frame += 1

            if self.animation_frame >= self.animation_steps:
                self.animation_frame = 0

        self.draw_bee(self.animation_list[self.animation_frame], position, screen)

        pygame.display.update()


    def draw_bee(self, bee_frame, position, screen):
        screen.blit(bee_frame, position)
        




NewGame = GameStartScreen()



NewGame.run()

    
pygame.quit()
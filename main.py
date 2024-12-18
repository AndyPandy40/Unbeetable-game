import pygame
pygame.init()

# Tile_size_constant
TILE_SIZE = 96

# Colour constants
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Function to make displaying text easier
def display_text(text, position, size, color, screen):

    text = str(text)
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

        # Sets up the screen
        self.screen = pygame.display.set_mode((self.screen_width, 960))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.run_start_screen = True
        self.run_game = False


        self.clock = pygame.time.Clock()
        
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

            # Display the menu at 120 fps
            self.display_menu()
            self.clock.tick(120)
            #print(self.clock.get_fps())




    def display_menu(self):
        #print("displaying menu")
        # Update start button
        self.start_button.draw_button(self.screen)

        # Update quit button
        self.quit_button.draw_button(self.screen)

        pygame.display.update()
        

    def display_game(self):

        # Creates a game class
        Game = MainGame(self.screen)
        
        # Stops the previous main loop from running
        self.run_start_screen = False
        Game.run_game()


    def quit(self):
        self.run_start_screen = False
        pygame.quit()
        exit()


class MainGame:
    def __init__(self, screen):

        # Sets up the screen
        self.screen = screen
        self.screen_width = 1440
        self.screen_height = 960
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()

        # Initialises and draws the tilemap
        self.NewMap = Map()
        self.NewMap.draw_tilemap(self.screen)

        # Initialises a bee
        self.Bee = Bees(48, BLACK, 100, 100, True, (850,900))

        self.NewMap.calc_tile_distances()
        

    def run_game(self):
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            #print(self.clock.get_fps())

            # Updates the tilemap and bee
            self.NewMap.draw_tilemap(self.screen)
            self.Bee.animate_bee(self.screen)
            
            self.NewMap.display_distances(self.screen)
            
            self.Bee.what_tile_am_I_on()

            # Display the game at 120 fps
            self.clock.tick(120)
            pygame.display.update()

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

        # Calculate the centre of the button
        self.button_center = ((self.position[0] + (self.width//2)), self.position[1] + (self.height//2))

    def draw_button(self, screen):
        # Get the position of the mouse and see if the user is clicking
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        # Check if user is hovering over button
        if self.position[0] < mouse[0] < self.position[0] + self.width and self.position[1] < mouse[1] < self.position[1] + self.height:
            button_color = self.active_color
            if click[0]:
                # Preform the button's action if the user clicks
                self.action()
        else:
            button_color = self.inactive_color

        # Draw a rectangle for the button
        pygame.draw.rect(screen, button_color, (self.position[0], self.position[1], self.width, self.height))
        
        # Display text on button
        display_text(self.text, self.button_center, 60, BLACK, screen)

class Map:
    def __init__(self):

        # Sets up the grass img
        self.grass_img = pygame.image.load("images/tiles/grass.png").convert()
        self.grass_img = pygame.transform.scale(self.grass_img, (TILE_SIZE, TILE_SIZE))

        # Sets up the path img
        self.path_img = pygame.image.load("images/tiles/path.png").convert()
        self.path_img = pygame.transform.scale(self.path_img, (TILE_SIZE, TILE_SIZE))

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

        # A dictionary to map the numbers (1 and 0) to their images
        self.tile_images = {
            0: self.grass_img,
            1: self.path_img,
        }

        # Set up everything for pathfinding
        self.frontier = []

        self.explored = []

        self.distances = {}

        self.target_tile = (14,4)


    def draw_tilemap(self, screen):
        # Iterates through each element in the 2d array
        for row in range(len(self.tilemap)):
            for col in range(len(self.tilemap[row])):
                # Finds the tile type at a position (1 or 0)
                tile_type = self.tilemap[row][col] 

                # Matches it with the image using the dictionary
                tile_image = self.tile_images[tile_type] 

                # Displays them in order using their position in the array and size
                screen.blit(tile_image, (col * TILE_SIZE, row * TILE_SIZE)) 

                # THIS COULD BE OPTIMISED TO ONLY BE DONE ONCE

    def calc_tile_distances(self):
        print("Target tile =", self.target_tile) # target is 14,4


        # The first tile has a distance of one
        self.distances[self.target_tile] = 0

        # Add the first tile to the frontier
        self.frontier.append(self.target_tile)

        # While there is something left in the frontier
        while len(self.frontier) != 0:
            # Check it hasn't already been calculated
            if self.frontier[0] not in self.explored:
                
                


                # Find the left, above right and below tile
                left_tile = ((self.frontier[0][0])-1, self.frontier[0][1])
                up_tile = (self.frontier[0][0], self.frontier[0][1]-1)
                right_tile = (self.frontier[0][0]+1, self.frontier[0][1])
                down_tile = (self.frontier[0][0], (self.frontier[0][1]+1))


                # Check if the tile we're appending is on the map and set it's distance to be one more than the current one
                if -1 < (left_tile[0]) < 14:
                    self.frontier.append(left_tile)
                    self.distances[left_tile] = (self.distances[self.frontier[0]] + 1)
                if -1 < (right_tile[0]) < 14:
                    self.frontier.append(right_tile)
                    self.distances[right_tile] = (self.distances[self.frontier[0]] + 1)
                if -1 < up_tile[1] < 9:
                    self.frontier.append(up_tile)
                    self.distances[up_tile] = (self.distances[self.frontier[0]] + 1)
                if -1 < down_tile[1] < 9:
                    self.frontier.append(down_tile)
                    self.distances[down_tile] = (self.distances[self.frontier[0]] + 1)


                # Say that is has already been explored once we're done with it
                self.explored.append(self.frontier[0])

                # Remove it from the queue as we've already explored it
                self.frontier.pop(0)


                print("tile_type:", self.check_if_field_tile(self.frontier[0]))

                #print("frontier:", self.frontier)
                #print(self.distances)
                #print("Explored nodes:", self.explored)
            
            else:

                # If it has been calculated remove it from the frontier
                self.frontier.pop(0)
                print("popped first item")


        
        print("final explored nodes:", self.explored)
        print("final distances", self.distances)


    def display_distances(self, screen):
        # Print distances on tiles
        for key in self.distances:
            text_x_pos = (key[0] * TILE_SIZE) + 50
            text_y_pos = (key[1]* TILE_SIZE) + 50
            display_text(str(self.distances[key]-2), (text_x_pos, text_y_pos), 50, BLACK, screen)

    def check_if_field_tile(self,tile):

        tile_x_pos = tile[0]
        tile_y_pos = tile[1]

        print(tile_x_pos)
        print(tile_y_pos)

        tile_type = self.tilemap[tile_y_pos][tile_x_pos]
        print(tile)
        if tile_type == 1:
            return True
        else:
            return False




class Bees:
    def __init__(self, size, color, health, speed, exists: bool, position):
        self.sprite_sheet = pygame.image.load("images/bees/bee.png").convert_alpha()
        self.size = size
        self.color = color
        self.health = health
        self.speed = speed
        self.exists = exists
        self.position = position

        # Set up everything needed for the animation
        self.animation_frame = 0
        self.animation_list = []
        self.animation_steps = 6
        self.animation_cooldown = 100

        self.last_update = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()

        # Loop through the sprite sheet
        for x in range(self.animation_steps):
            # Get the inividual frames for the bee and append them to an array
            self.animation_list.append(self.get_image(x, self.size, self.size))
            #print("frame", x, "appended to list")


    def get_image(self, level, width, height):

        # Create a surface to blit the image onto
        image = pygame.Surface((width, height))

        # Blit the frame of the bee onto the surface
        image.blit(self.sprite_sheet, (0,0), ((level*width, 0, width, height)))

        # Make the background transparent
        image.set_colorkey(self.color)

        return image
    
    def animate_bee(self, screen):

        self.current_time = pygame.time.get_ticks()

        # Check if it's time to update the frame
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.last_update = self.current_time

            # Go to the next frame in the animation
            self.animation_frame += 1

            if self.animation_frame >= self.animation_steps:
                # Loop back to the first frame if it goes over the animation steps
                self.animation_frame = 0
                #print("reseting animation")

        # Displays the current animation frame on the screen
        screen.blit(self.animation_list[self.animation_frame], self.position)

        pygame.display.update()

    def what_tile_am_I_on(self):
        x_tile = self.position[0] // TILE_SIZE

        y_tile = self.position[1] // TILE_SIZE

        #print("my position is", self.position[0], self.position[1])
        #print("I am on x tile", x_tile)
        #print("I am on y tile", y_tile)

# Initialises and starts the starting screen
NewGame = GameStartScreen()
NewGame.run()

    
pygame.quit()
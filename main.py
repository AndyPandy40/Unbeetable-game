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
YELLOW = (225, 225, 0)
GRAY = (146, 142, 135)

# Function to make displaying text easier
def display_text(text, position, size, color, screen):

    text = str(text).strip()
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
        self.screen = pygame.display.set_mode((1824, 960))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.run_start_screen = True
        self.run_game = False


        self.clock = pygame.time.Clock()
        
        # Displays background images and text
        self.screen.blit(self.background_color_image, (0,0))
        self.screen.blit(self.bee_background_image, (0,0))
        self.screen.blit(self.title_text, (80,20))


        # Displays buttons at start of code
        self.start_button = Button(self.screen, GREEN, LIGHT_GREEN, "Start", (216, 550), 450, 100, 60, self.display_game)
        self.quit_button = Button(self.screen, RED, LIGHT_RED, "Quit", (774, 550), 450, 100, 60, self.quit)



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
        self.screen_width = 1824
        self.screen_height = 960
        self.game_width = 1440
        self.game_height = self.screen_height

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.heart_image =  pygame.image.load("images/heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (27, 27))
        

        self.clock = pygame.time.Clock()
        self.game_start_time = pygame.time.get_ticks()

        # Initialises and draws the tilemap
        self.NewMap = Map()
        self.NewMap.draw_tilemap(self.screen)

        # Creates the shop
        pygame.draw.rect(self.screen, GRAY, (self.game_width, 0, TILE_SIZE*4, self.game_height))
        pygame.draw.line(self.screen, BLACK, (self.game_width+4, 0), (self.game_width+4, self.screen_height), 10)
        display_text("SHOP", (self.game_width + TILE_SIZE*2, TILE_SIZE/2), 50, BLACK, self.screen)
        pygame.draw.line(self.screen, BLACK, (self.game_width+4, TILE_SIZE), (self.screen_width, TILE_SIZE), 10)

        # Create button for tower
        self.TowerButton = Button(self.screen, (10, 178, 21), LIGHT_GREEN, "100", (self.game_width+35, TILE_SIZE+30), 320, 75, 35, self.buy_tower)
        self.TowerButton.draw_button(self.screen)


        # Display tower image on button
        self.shop_tower_height = TILE_SIZE*0.75
        self.shop_tower_width = self.shop_tower_height//3

        self.tower_image = pygame.image.load("images/towers/towerBase.png")
        self.shop_tower_image = pygame.transform.scale(self.tower_image, (self.shop_tower_height+45, self.shop_tower_height))

        self.screen.blit(self.shop_tower_image, (self.game_width + 70, TILE_SIZE + 25), (0, 0, self.shop_tower_width + 15, self.shop_tower_height))
        

        # Display coin image on button
        self.shop_coin_image = pygame.image.load("images/coin.png")
        self.shop_coin_image = pygame.transform.scale_by(self.shop_coin_image, 0.6)

        self.screen.blit(self.shop_coin_image, (self.game_width + 136, 148))
        

        

        # Set up spawning bees
        self.bee_array = []
        self.last_bee_spawned = 0
        self.bee_spawn_cooldown = 2000


        self.NewMap.calc_tile_distances()
        self.mapVectors = self.NewMap.get_vectors()


        self.score = 0
        self.money = 10000
        self.lives = 5

        self.placing_tower = False

        self.tower_array = []

        self.ghost_tower_x_pos = 0
        self.ghost_tower_y_pos = 0
        

    def run_game(self):
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.placing_tower == True:
                    self.place_tower()
                

            #print(self.clock.get_fps())

            # Updates the tilemap and bee
            self.NewMap.draw_tilemap(self.screen)
            
            
            #self.NewMap.display_distances(self.screen)

            #self.NewMap.display_tile_positions(self.screen)

            #self.NewMap.display_vectors(self.screen)

            self.display_score()
            self.display_money()
            self.display_lives()

            self.current_time = pygame.time.get_ticks()

            self.bee_spawn_cooldown -= self.current_time/80000

            if self.bee_spawn_cooldown <= 500:
                self.bee_spawn_cooldown = 500

            if self.current_time - self.last_bee_spawned >= self.bee_spawn_cooldown:
                self.last_bee_spawned = self.current_time

                TopBee = Bees(48, BLACK, 100, 1, True, (0,350))
                BottomBee = Bees(48, BLACK, 100, 1, True, (0,650))
                self.bee_array.append(TopBee)
                self.bee_array.append(BottomBee)


            for entity in self.bee_array:
                if entity.position[0] >= self.game_width-5:
                    entity.exists = False
                    self.lives -= 1

                self.current_time = pygame.time.get_ticks()

                if not entity.exists:
                    self.bee_array.remove(entity)


                bee_tile = entity.what_tile_am_I_on()
                bee_vector = self.mapVectors[bee_tile]
                bee_vector = (bee_vector[0]*entity.speed,bee_vector[1] * entity.speed)

                entity.change_position(bee_vector[0], bee_vector[1])

                entity.animate_bee(self.screen)

                # Blits the line again to draw over dead bees
                pygame.draw.line(self.screen, BLACK, (self.game_width+4, 0), (self.game_width+4, self.screen_height), 10)

                # Redraw shop button
                self.TowerButton.draw_button(self.screen)
                self.display_shop_button_images()

                if self.placing_tower == True:
                    self.display_ghost_tower()

                # Draw all of the towers
                for tower in  self.tower_array:
                    tower.draw_tower(self.screen)


            self.mouse_pos = pygame.mouse.get_pos()
            self.clicked = pygame.mouse.get_pressed()

            # Display the game at 120 fps
            self.clock.tick(120)
            pygame.display.update()



    def display_score(self):
        score_string = ("Score: " + str(self.score))
        display_text(score_string, (80, 40), 25, YELLOW, self.screen)


    def display_money(self):
        money_string = (self.money)
        display_text(money_string, (1140, 42), 25, YELLOW, self.screen)
        self.screen.blit(self.shop_coin_image, (1085, 26))


    def display_lives(self):
        lives_string = (str(self.lives)+"/5")
        display_text(lives_string, (1330, 42), 25, RED, self.screen)
        self.screen.blit(self.heart_image, (1280, 25))


    def display_shop_button_images(self):
        # Display tower
        self.screen.blit(self.shop_tower_image, (self.game_width + 70, TILE_SIZE + 25), (0, 0, self.shop_tower_width + 15, self.shop_tower_height))

        # Display coin image
        self.screen.blit(self.shop_coin_image, (self.game_width + 136, 148))



    def buy_tower(self):
        #Check if player has enough money
        if self.placing_tower == False:
            if self.money >= 100:
                self.money -= 100
                self.placing_tower = True
                
                self.display_ghost_tower()

    def display_ghost_tower(self):
        ghost_tower_image = pygame.transform.scale(self.tower_image, (TILE_SIZE*1.5, TILE_SIZE))
        ghost_tower_image.set_alpha(20)

        ghost_tower_height = TILE_SIZE
        ghost_tower_width = TILE_SIZE / 2


        self.ghost_tower_x_pos = ((self.mouse_pos[0] // TILE_SIZE) * TILE_SIZE) + TILE_SIZE//4
        self.ghost_tower_y_pos = ((self.mouse_pos[1] // TILE_SIZE) * TILE_SIZE) - TILE_SIZE//3

        if not self.ghost_tower_x_pos >= self.game_width:
            self.screen.blit(ghost_tower_image, [self.ghost_tower_x_pos, self.ghost_tower_y_pos], (0, 0, ghost_tower_width , ghost_tower_height))

        return


    def place_tower(self):
        if self.ghost_tower_x_pos <= self.game_width:
            NewTower = Towers((self.ghost_tower_x_pos, self.ghost_tower_y_pos), BLACK)
            self.tower_array.append(NewTower)


            self.placing_tower = False
        

    def quit(self):
        pygame.quit()
        exit()


class Button:
    def __init__(self, screen, inactive_color, active_color, text, position, width, height, text_size, action=None):
        self.screen = screen
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.text_size = text_size
        self.action = action

        # Calculate the centre of the button
        self.button_center = ((self.position[0] + (self.width//2)), self.position[1] + (self.height//2))

        pygame.draw.rect(screen, self.inactive_color, (self.position[0], self.position[1], self.width, self.height), 0, 15)
        display_text(self.text, self.button_center, self.text_size, BLACK, screen)

        self.last_update = False
        self.current_update = False

    def draw_button(self, screen):
        # Get the position of the mouse and see if the user is clicking
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        # Check if user is hovering over button
        if self.position[0] < mouse[0] < self.position[0] + self.width and self.position[1] < mouse[1] < self.position[1] + self.height:
            self.current_update = True
            button_color = self.active_color
            if click[0]:
                # Preform the button's action if the user clicks
                self.action()
        else:
            button_color = self.inactive_color
            self.current_update = False


        if self.current_update != self.last_update:
            # Draw a rectangle for the button
            pygame.draw.rect(screen, button_color, (self.position[0], self.position[1], self.width, self.height), 0, 15)
            
            # Display text on button
            display_text(self.text, self.button_center, self.text_size, BLACK, screen)

        self.last_update = self.current_update


class Map:
    def __init__(self):

        # Sets up the grass img
        self.grass_img = pygame.image.load("images/tiles/grass.png").convert()
        self.grass_img = pygame.transform.scale(self.grass_img, (TILE_SIZE, TILE_SIZE))

        # Sets up the path img
        self.path_img = pygame.image.load("images/tiles/path.png").convert()
        self.path_img = pygame.transform.scale(self.path_img, (TILE_SIZE, TILE_SIZE))

        # A dictionary to map the numbers (1 and 0) to their images
        self.tile_images = {
            0: self.grass_img,
            1: self.path_img,
        }

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

        self.background_surface = pygame.Surface((1440, 960))

        for row in range(len(self.tilemap)):
            for col in range(len(self.tilemap[row])):
                # Finds the tile type at a position (1 or 0)
                tile_type = self.tilemap[row][col] 

                # Matches it with the image using the dictionary
                tile_image = self.tile_images[tile_type] 

                # Displays them in order using their position in the array and size
                if col != 15:
                    self.background_surface.blit(tile_image, (col * TILE_SIZE, row * TILE_SIZE)) 




        # Set up everything for pathfinding
        self.frontier = []
        self.distances = {}
        self.target_tile = (15,4)
        self.explored = []

        self.vectors= {}


    def draw_tilemap(self, screen):
        
        screen.blit(self.background_surface, (0, 0))

    def calc_tile_distances(self):
        #print("Target tile =", self.target_tile) # target is 15,4


        # The first tile has a distance of one
        self.distances[self.target_tile] = 0

        # Add the first tile to the frontier
        self.frontier.append(self.target_tile)

        # While there is something left in the frontier
        while (self.frontier):
            if self.check_if_field_tile(self.frontier[0]) == True:
                self.distances[self.frontier[0]] = 99
                self.frontier.pop(0)

            # Check it hasn't already been calculated
            else:
                if self.frontier[0] not in self.explored:
                    # Find the left, above right and below tile
                    left_tile = ((self.frontier[0][0])-1, self.frontier[0][1])
                    up_tile = (self.frontier[0][0], self.frontier[0][1]-1)
                    right_tile = (self.frontier[0][0]+1, self.frontier[0][1])
                    down_tile = (self.frontier[0][0], (self.frontier[0][1]+1))


                    # Check if the tile we're appending is on the map and set it's distance to be one more than the current one
                    if (-1 < (left_tile[0]) < 15) and left_tile not in self.explored:
                        self.frontier.append(left_tile)
                        self.distances[left_tile] = (self.distances[self.frontier[0]] + 1)
                    if (-1 < (right_tile[0]) < 15) and right_tile not in self.explored:
                        self.frontier.append(right_tile)
                        self.distances[right_tile] = (self.distances[self.frontier[0]] + 1)
                    if (-1 < up_tile[1] < 10) and up_tile not in self.explored:
                        self.frontier.append(up_tile)
                        self.distances[up_tile] = (self.distances[self.frontier[0]] + 1)
                    if (-1 < down_tile[1] < 10) and down_tile not in self.explored:
                        self.frontier.append(down_tile)
                        self.distances[down_tile] = (self.distances[self.frontier[0]] + 1)


                    # Say that is has already been explored once we're done with it
                    self.explored.append(self.frontier[0])
                    print(self.frontier[0], "is explored")

                    # Remove it from the queue as we've already explored it
                    self.frontier.pop(0)

                    #print("frontier:", self.frontier)
                    #print(self.distances)
                    
                else:

                    # If it has been calculated remove it from the frontier
                    self.frontier.pop(0)
        
        for key in self.distances:
            vector = self.find_tile_vector(key)
            self.vectors[key] = vector
           

        

        #print("final distances", self.distances)

    def find_tile_vector(self, key):

        # Define the neighbouring tiles and their directions
        neighbours = [
            ((key[0] - 1, key[1]), (-1, 0)),  # Left
            ((key[0], key[1] - 1), (0, -1)),  # Up
            ((key[0] + 1, key[1]), (1, 0)),   # Right
            ((key[0], key[1] + 1), (0, 1)),   # Down
        ]

        closest_tile = None
        smallest_distance = 9999  # Start with a very large distance

        for tile, direction in neighbours:
            if tile in self.distances:  # Check if the tile has a distance
                distance = self.distances[tile]
                if distance < smallest_distance:  # Update closest tile if smaller distance is found
                    smallest_distance = distance # This is the new closest distance

                    # Use the dictionary to return the vector for the distance
                    closest_tile = direction 

        return closest_tile


    def display_distances(self, screen):
        # Print distances on tiles
        for key in self.distances:
            text_x_pos = (key[0] * TILE_SIZE) + 50
            text_y_pos = (key[1]* TILE_SIZE) + 50
            display_text(str(self.distances[key]), (text_x_pos, text_y_pos), 50, BLACK, screen)

    def display_tile_positions(self, screen):
        for key in self.distances:
            text_x_pos = (key[0] * TILE_SIZE) + 50
            text_y_pos = (key[1]* TILE_SIZE) + 50
            coords = f"({key[0]}, {key[1]})" 
            display_text(coords, (text_x_pos, text_y_pos), 32, BLACK, screen)

    def display_vectors(self, screen):
        for vector in self.vectors:
            text_x_pos = (vector[0] * TILE_SIZE) + 50
            text_y_pos = (vector[1]* TILE_SIZE) + 50
            display_text(str(self.vectors[vector]), (text_x_pos, text_y_pos), 32, BLACK, screen)

    def check_if_field_tile(self,tile):

        tile_y_pos = tile[0]
        tile_x_pos = tile[1]

        #print(tile_x_pos)
        #print(tile_y_pos)

        tile_type = self.tilemap[tile_x_pos][tile_y_pos]
        #print(tile)
        if tile_type == 0:
            return True
        else:
            return False
    
    def get_vectors(self):
        return self.vectors



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

        # Set up properties for bee pathfinding frequency
        self.last_movement_update = 0


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
        screen.blit(self.animation_list[self.animation_frame], (self.position[0] - self.size// 2, self.position[1]- self.size//2))



    def what_tile_am_I_on(self):
        x_tile = self.position[0] // TILE_SIZE

        y_tile = self.position[1] // TILE_SIZE

        return (x_tile, y_tile)

        #print("my position is", self.position[0], self.position[1])
        #print("I am on x tile", x_tile)
        #print("I am on y tile", y_tile)

    def change_position(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[1] + dy)



class Towers:
    def __init__(self, position, color):
        self.sprite_sheet = pygame.image.load("images/towers/towerBase.png")
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (TILE_SIZE*1.5, TILE_SIZE))

        self.weapon_sprite_sheet = pygame.image.load("images/towers/towerWeapon.png")
        self.weapon_sprite_sheet = pygame.transform.scale_by(self.weapon_sprite_sheet, 1)

        self.position = position

        self.color = color

        self.tower_height = TILE_SIZE 
        self.tower_width = TILE_SIZE / 2

        self.level = 1

        self.tower_animation_frame = 0
        self.tower_animation_list = []
        self.tower_animation_steps = 10
        self.tower_animation_cooldown = 100

        self.weapon_size = 48

        self.last_update = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()

        # Loop through the sprite sheet
        for x in range(self.tower_animation_steps):
            # Get the inividual frames for the bee and append them to an array
            self.tower_animation_list.append(self.get_weapon_image(x, self.weapon_size, self.weapon_size))
            #print("frame", x, "appended to list")
            
        self.weapon_position = (self.position[0], self.position[1] + 30)
        

    def draw_tower(self, screen):
        
        tower_x_pos = self.position[0]
        tower_y_pos = self.position[1]

        screen.blit(self.sprite_sheet, (tower_x_pos, tower_y_pos), ((self.level-1)*(self.tower_width), 0, self.tower_width , self.tower_height))

        self.animate_weapon(screen)

    def get_weapon_image(self, frame, width, height):

        image = pygame.Surface((width, height))

        # Blit the frame of the bee onto the surface
        image.blit(self.weapon_sprite_sheet, (0,0), ((frame*width, 0, width, height)))

        image.set_colorkey(self.color)

        return image
    
    def animate_weapon(self, screen):

        self.current_time = pygame.time.get_ticks()

        # Check if it's time to update the frame
        if self.current_time - self.last_update >= self.tower_animation_cooldown:
            self.last_update = self.current_time

            # Go to the next frame in the animation
            self.tower_animation_frame += 1

            if self.tower_animation_frame >= self.tower_animation_steps:
                # Loop back to the first frame if it goes over the animation steps
                self.tower_animation_frame = 0
                #print("reseting animation")

        # Displays the current animation frame on the screen
        screen.blit(self.tower_animation_list[self.tower_animation_frame], (self.position[0] - self.weapon_size// 2, self.weapon_position[1]- self.weapon_size//2))




# Initialises and starts the starting screen
NewGame = GameStartScreen()
NewGame.run()
    
pygame.quit()
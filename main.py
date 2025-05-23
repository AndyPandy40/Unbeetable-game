import pygame
import copy
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

        self.tilemap = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
            [0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
            [0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
            [0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]


        bee_target_tile = (15,4)
        upper_bee_starting_tile = (0, 3)
        lower_bee_starting_tile = (0, 6)
        self.NewMap = Map(bee_target_tile, upper_bee_starting_tile, lower_bee_starting_tile, self.tilemap)
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
        self.bee_spawn_cooldown = 4000
        self.bee_health = 250
        self.number_of_bees_spawned = 0

        # Calculate all the tile vectors
        self.NewMap.calc_tile_distances(self.tilemap)
        self.mapVectors = self.NewMap.get_vectors()

        self.score = 0
        self.money = 1000
        self.lives = 5

        # Not currently placing tower
        self.placing_tower = False

        # Set up towers
        self.tower_array = []

        self.tower_places = copy.deepcopy(self.tilemap)

        self.ghost_tower_x_pos = 0
        self.ghost_tower_y_pos = 0
        

    def run_game(self):
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.placing_tower == True:
                        self.check_tower()

                    if event.button == 3:
                        right_clicked = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and self.placing_tower == False:
                        self.buy_tower()

                    if event.key == pygame.K_ESCAPE and self.placing_tower == True:
                        self.placing_tower = False

                    if event.key == pygame.K_p:
                        self.pause_game()

            self.mouse_pos = pygame.mouse.get_pos()
            self.clicked = pygame.mouse.get_pressed()

            if self.lives == 0:
                print(self.score)
                        
                
            # Show fps
            #print(self.clock.get_fps())

            original_clip = self.screen.get_clip()
            self.screen.set_clip((0, 0, self.game_width, self.game_height))


            # Updates the tilemap and bees
            self.NewMap.draw_tilemap(self.screen)

            self.current_time = pygame.time.get_ticks()


            # Slowly decrease bee spawn time
            self.bee_spawn_cooldown -= self.current_time/1000000

            if self.bee_spawn_cooldown <= 400:
                self.bee_spawn_cooldown = 400

            # Spawn a bee at the top and bottom of the map
            if self.current_time - self.last_bee_spawned >= self.bee_spawn_cooldown:
                self.last_bee_spawned = self.current_time

                self.number_of_bees_spawned += 2

                if self.number_of_bees_spawned % 10 == 0:
                    self.bee_health += 10

                

                TopBee = Bees(48, BLACK, self.bee_health, 0.5, True, (0,350))
                BottomBee = Bees(48, BLACK, self.bee_health, 0.5, True, (0,650))
                self.bee_array.append(TopBee)
                self.bee_array.append(BottomBee)

            
            for entity in self.bee_array:
                # If a bee reaches the end of the map
                if entity.position[0] >= self.game_width-5:

                    # Kill the bee
                    entity.exists = False

                    # Remove one life
                    self.lives -= 1

                self.current_time = pygame.time.get_ticks()

                # Remove any dead bees from the bee array
                if not entity.exists:
                    self.bee_array.remove(entity)


                # Move each bee based on the vector of the tile they're on
                bee_tile = entity.what_tile_am_I_on()
                tile_bee_vector = self.mapVectors[bee_tile]

                bee_tile = pygame.Vector2(bee_tile)
                tile_bee_vector = pygame.Vector2(tile_bee_vector)

                # Find the next tile the bee will try go to
                next_tile = bee_tile + tile_bee_vector
                
                # Find the center of the next tile
                next_tile_center_pos = TILE_SIZE * (next_tile + pygame.Vector2(0.5, 0.5))

                # Find the direction to the center of the next tile
                bee_direction = next_tile_center_pos - pygame.Vector2(entity.get_position())
                bee_vector = bee_direction.normalize() * entity.speed
                
                # Change the bee's location based on the vector
                entity.change_position(bee_vector[0], bee_vector[1])



                # Animate each bee
                entity.animate_bee(self.screen)

            # Blits the line again to draw over dead bees
            pygame.draw.line(self.screen, BLACK, (self.game_width+4, 0), (self.game_width+4, self.screen_height), 10)



            # Display ghost tower if buying tower
            if self.placing_tower == True:
                self.display_ghost_tower()

            # Update all of the towers
            for tower in self.tower_array:
                tower.draw_tower(self.screen)

                # If the tower kills the bee
                if tower.try_to_shoot_bee(self.bee_array, self.screen):
                    self.score += 5
                    self.money += 10


                change_in_money = tower.am_i_being_hovered(self.mouse_pos, right_clicked, self.screen, self.money)

                if change_in_money != None:
                    self.money += change_in_money

            self.screen.set_clip(original_clip)

            self.display_score()
            self.display_money()
            self.display_lives()

            # Redraw shop button
            self.TowerButton.draw_button(self.screen)
            self.display_shop_button_images()

            #self.NewMap.display_distances(self.screen)


            right_clicked = False

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
                
                self.placing_tower = True
                
                self.display_ghost_tower()


    def display_ghost_tower(self):
        ghost_tower_image = pygame.transform.scale(self.tower_image, (TILE_SIZE*1.5, TILE_SIZE))
        ghost_tower_image.set_alpha(60)

        ghost_tower_height = TILE_SIZE
        ghost_tower_width = TILE_SIZE / 2


        self.ghost_tower_x_pos = ((self.mouse_pos[0] // TILE_SIZE) * TILE_SIZE) + TILE_SIZE//4
        self.ghost_tower_y_pos = ((self.mouse_pos[1] // TILE_SIZE) * TILE_SIZE) - TILE_SIZE//3

        if not self.ghost_tower_x_pos >= self.game_width:
            self.screen.blit(ghost_tower_image, [self.ghost_tower_x_pos, self.ghost_tower_y_pos], (0, 0, ghost_tower_width , ghost_tower_height))


    def check_tower(self):
        if self.ghost_tower_x_pos <= self.game_width:
            x_tile = self.ghost_tower_x_pos // TILE_SIZE
            y_tile = (self.ghost_tower_y_pos // TILE_SIZE) + 1

            if self.tower_places[y_tile][x_tile] == 2:
                return

            if self.tower_places[y_tile][x_tile] == 1:
                is_valid_placement, new_tile_vectors = self.NewMap.check_valid_placement(y_tile, x_tile)

                if not is_valid_placement:
                    return
                
                else:
                    self.mapVectors = new_tile_vectors
                    self.place_tower(x_tile, y_tile)
                    return

            self.place_tower(x_tile, y_tile)


    def place_tower(self, x_tile, y_tile):

        NewTower = Towers((self.ghost_tower_x_pos, self.ghost_tower_y_pos), BLACK, 50, (x_tile, y_tile))
        self.tower_array.append(NewTower)

        self.tower_places[y_tile][x_tile] = 2
        self.money -= 100
        self.placing_tower = False


    def get_money(self):
        return self.money
    
    def change_money(self, change):
        self.money += change

    def pause_game(self):
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                if event.type == pygame.QUIT:
                    self.quit()

        
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
    def __init__(self, target_tile, bee_starting_tile1, bee_starting_tile2, tilemap):

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

        self.background_surface = pygame.Surface((1440, 960))

        self.tilemap = tilemap

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
        self.target_tile = target_tile
        self.bee_starting_tile1 = bee_starting_tile1
        self.bee_starting_tile2 = bee_starting_tile2
        self.explored = []
        self.distances = {}
        self.vectors= {}


    def draw_tilemap(self, screen):
        screen.blit(self.background_surface, (0, 0))

    def calc_tile_distances(self, tilemap):
        # target tile is 15,4

        self.explored = []
        self.distances = {}
        self.vectors = {}
        self.frontier = []

        # The first tile has a distance of one
        self.distances[self.target_tile] = 0

        # Add the first tile to the frontier
        self.frontier.append(self.target_tile)

        # While there is something left in the frontier
        while (self.frontier):
            if self.check_if_field_tile(self.frontier[0], tilemap) == True:
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

                    # Remove it from the queue as we've already explored it
                    self.frontier.pop(0)
                    
                else:

                    # If it has been calculated remove it from the frontier
                    self.frontier.pop(0)
        
        for key in self.distances:
            vector = self.find_tile_vector(key)
            self.vectors[key] = vector

        if (self.bee_starting_tile1 in self.vectors) and (self.bee_starting_tile2 in self.vectors):
            return True
        else:
            return False
           

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


    def check_if_field_tile(self, tile, tile_map):

        tile_y_pos = tile[0]
        tile_x_pos = tile[1]

        tile_type = tile_map[tile_x_pos][tile_y_pos]

        if tile_type != 1:
            return True
        else:
            return False

    
    def check_valid_placement(self, y_tile, x_tile):

        previous_map = copy.deepcopy(self.tilemap)


        new_map = self.tilemap
        
        new_map[y_tile][x_tile] = 0

        if self.calc_tile_distances(new_map):
            return True, self.vectors
        
        else:
            self.tilemap = previous_map


            return False, None


    def display_distances(self, screen):
        # Print distances on tiles
        for key in self.distances:
            text_x_pos = (key[0] * TILE_SIZE) + 50
            text_y_pos = (key[1] * TILE_SIZE) + 50
            display_text(str(self.distances[key]), (text_x_pos, text_y_pos), 50, BLACK, screen)

    def display_tile_positions(self, screen):
        for key in self.distances:
            text_x_pos = (key[0] * TILE_SIZE) + 50
            text_y_pos = (key[1] * TILE_SIZE) + 50
            coords = f"({key[0]}, {key[1]})" 
            display_text(coords, (text_x_pos, text_y_pos), 32, BLACK, screen)

    def display_vectors(self, screen):
        for vector in self.vectors:
            text_x_pos = (vector[0] * TILE_SIZE) + 50
            text_y_pos = (vector[1]* TILE_SIZE) + 50
            display_text(str(self.vectors[vector]), (text_x_pos, text_y_pos), 32, BLACK, screen)



    def get_vectors(self):
        return self.vectors

    def get_tilemap(self):
        return self.tilemap


class Bees:
    def __init__(self, size, color, health, speed, exists: bool, position):
        self.sprite_sheet = pygame.image.load("images/bees/bee.png").convert_alpha()
        self.size = size
        self.color = color 
        self.health = health
        self.original_health = self.health
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

        self.showing_health_bar = False


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

        if self.health != self.original_health:
            self.showing_health_bar = True 

        # Check if it's time to update the frame
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.last_update = self.current_time

            # Go to the next frame in the animation
            self.animation_frame += 1

            if self.animation_frame >= self.animation_steps:
                # Loop back to the first frame if it goes over the animation steps
                self.animation_frame = 0
                #print("reseting animation")

        if self.showing_health_bar == True:
            self.display_health_bar(screen)

        # Displays the current animation frame on the screen
        screen.blit(self.animation_list[self.animation_frame], (self.position[0] - self.size// 2, self.position[1]- self.size//2))
        



    def display_health_bar(self, screen):

        red_rectangle_length = 20
        rectangle_height = 2

        green_rectangle_length = red_rectangle_length * (self.health/self.original_health)

        health_bar_location = self.position[0] - red_rectangle_length // 2, self.position[1] - 10

        pygame.draw.rect(screen, RED, (health_bar_location[0], health_bar_location[1], red_rectangle_length, rectangle_height))
        pygame.draw.rect(screen, GREEN, (health_bar_location[0], health_bar_location[1], green_rectangle_length, rectangle_height))


    def what_tile_am_I_on(self):
        x_tile = self.position[0] // TILE_SIZE

        y_tile = self.position[1] // TILE_SIZE

        return (x_tile, y_tile)

        #print("my position is", self.position[0], self.position[1])
        #print("I am on x tile", x_tile)
        #print("I am on y tile", y_tile)

    def change_position(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def reduce_health(self, damage):
        # Deal damage
        self.health -= damage

        # If the bee is killed
        if self.health <= 0:
            self.exists = False

            return True
        return False
    
    def get_x_position(self):
        return self.position[0]
    
    def get_y_position(self):
        return self.position[1]
    
    def get_position(self):
        return self.position
    
    
    def get_size(self):
        return self.size
    
    def does_exist(self):
        return self.exists
    
    def get_x_center(self):
        return self.bee_x_center
    
    def get_y_center(self):
        return self.bee_y_center


class Towers:
    def __init__(self, position, color, damage, tile):
        self.sprite_sheet = pygame.image.load("images/towers/towerBase.png")
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (TILE_SIZE*1.5, TILE_SIZE))

        self.weapon_sprite_sheet = pygame.image.load("images/towers/towerWeapon.png")
        self.weapon_sprite_sheet = pygame.transform.scale_by(self.weapon_sprite_sheet, 1)

        self.position = position
        self.color = color
        self.damage = damage
        self.tile = tile


        self.tower_height = TILE_SIZE 
        self.tower_width = TILE_SIZE // 2

        # Tower starts on level 1
        self.level = 1

        # Tower has a range of square root of 150
        self.tower_range = 150

        # Set up tower idle animation
        self.tower_animation_frame = 0
        self.tower_animation_list = []
        self.tower_animation_steps = 10
        self.tower_animation_cooldown = 200
        self.tower_column = 0

        # Set up tower attack animation
        self.attack_animation_frame = 0
        self.attack_animation_list = []
        self.attack_animation_steps = 16
        self.attack_animation_cooldown = 100
        self.attack_column = 1

        self.weapon_size = 48

        # Set up times for animation
        self.last_update = pygame.time.get_ticks()
        self.current_time = self.last_update
        self.last_attack_update = self.current_time

        # Set up the center of tower
        self.tower_x_center = (self.position[0] - TILE_SIZE//4 + TILE_SIZE//2)
        self.tower_y_center = (self.position[1] + TILE_SIZE//1.5 + 15)
        

        # Loop through the sprite sheet
        for x in range(self.tower_animation_steps):
            # Get the inividual frames for the tower  and append them to an array
            self.tower_animation_list.append(self.get_weapon_image(x, self.weapon_size, self.weapon_size, self.tower_column))

        # Loop through attack sprite sheet and get the frames
        for y in range(self.attack_animation_steps):
            self.attack_animation_list.append(self.get_weapon_image(y, self.weapon_size, self.weapon_size, self.attack_column))
            
        # Set the weapon position to be just above the tower
        self.weapon_position = (self.position[0] - self.weapon_size// 2 + TILE_SIZE//4, self.position[1] + 30 - self.weapon_size//2)

        self.shooting_bee = False
        self.killed_bee = False

        

    def get_weapon_image(self, frame, width, height, column):

        image = pygame.Surface((width, height))

        # Blit the frame of the bee onto the surface
        image.blit(self.weapon_sprite_sheet, (0,0), ((frame*width, height*column, width, height)))

        image.set_colorkey(self.color)

        return image


    def draw_tower(self, screen):
        
        tower_x_pos = self.position[0]
        tower_y_pos = self.position[1]

        screen.blit(self.sprite_sheet, (tower_x_pos, tower_y_pos), ((self.level-1)*(self.tower_width), 0, self.tower_width , self.tower_height))

        # Play correct weapon aniumation
        if not self.shooting_bee:
            self.animate_weapon(screen)
        else:
            self.play_shoot_animation(screen)


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

        # Displays the current animation frame on the screen
        screen.blit(self.tower_animation_list[self.tower_animation_frame], (self.weapon_position[0], self.weapon_position[1]))


    def try_to_shoot_bee(self, bees, screen):

        # Could check tiles around the tower first



        nearby_bees = []

        for bee in bees:
            # Find the squared distance to the bee
            x_dist_squared = (bee.position[0] - self.tower_x_center)**2
            y_dist_squared = (bee.position[1] - self.tower_y_center)**2

            # If the bee is in range append it to an array
            if x_dist_squared + y_dist_squared <= self.tower_range**2:
                nearby_bees.append(bee)

        

        # Check if there is a bee nearby
        if nearby_bees:
            # And if the tower isn't already shooting a bee
            if self.shooting_bee == False:

                    self.shooting_bee = True

                    self.current_bee_under_attack = nearby_bees[0]

                    # If a bee has been killed return True so score and money can be added
                    if self.killed_bee:
                        self.killed_bee = False
                        return True

    def play_shoot_animation(self, screen):

        if self.current_bee_under_attack.does_exist():
            self.current_time = pygame.time.get_ticks()

            

            if self.current_time - self.last_attack_update >= self.attack_animation_cooldown:
                self.last_attack_update = self.current_time
                
                self.attack_animation_frame += 1

                if self.attack_animation_frame >= self.attack_animation_steps:
                    self.attack_animation_frame = 0

                    # If the animation is over a bee is no longer being shot
                    self.shooting_bee = False

                    # Deal the damage to the bee
                    if self.current_bee_under_attack.reduce_health(self.damage):

                        self.killed_bee = True

            
            # Draw the weapon image 0.8x the size
            scale_factor = 0.8

            # Scale the previous weapon image b the scale factor
            current_surface = self.attack_animation_list[self.attack_animation_frame]
            scaled_surface = pygame.transform.scale_by(current_surface, scale_factor)

            # Get the original image size
            old_surface_size = current_surface.get_size()[1]

            position_difference = (1-scale_factor) * old_surface_size

            # Calculate the center of the bee
            bee_x_position = self.current_bee_under_attack.get_x_position() - (self.current_bee_under_attack.get_size() // 2) + (position_difference // 2)
            bee_y_position = self.current_bee_under_attack.get_y_position() - (self.current_bee_under_attack.get_size() // 2) + (position_difference // 2)


            # Blit the scaled attack animation frame onto the bee
            screen.blit(scaled_surface, (bee_x_position, bee_y_position))

            # Blit the tower animation after
            screen.blit(self.attack_animation_list[self.attack_animation_frame], (self.weapon_position[0], self.weapon_position[1]))

            #pygame.draw.line(screen, WHITE, (self.tower_x_center, self.tower_y_center), (int(bee_x_position), int(bee_y_position)))

        else:
            self.shooting_bee = False


    def am_i_being_hovered(self, mouse_pos, right_clicked, screen, money):

        tile_top_left = self.tile[0] * TILE_SIZE, self.tile[1] * TILE_SIZE
        change_money = 0

        if tile_top_left[0] < mouse_pos[0] < tile_top_left[0] + TILE_SIZE:
            if tile_top_left[1] < mouse_pos[1] < tile_top_left[1] + TILE_SIZE:
                if right_clicked:
                    if self.upgrade_tower(money):
                        change_money = -300
        
                # Show the tower's range
                circle_surface = pygame.Surface((self.tower_range*2, self.tower_range*2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (0, 0, 0, 40), (self.tower_range, self.tower_range), self.tower_range)
                screen.blit(circle_surface, (self.tower_x_center - self.tower_range, self.tower_y_center-self.tower_range))

                return change_money

    def upgrade_tower(self, money):
        if self.level != 3 and money >= 300:
            new_weapon_pos = self.weapon_position[0], self.weapon_position[1] - 5
            self.weapon_position = new_weapon_pos
            self.level += 1

            # Upgrades
            self.damage += 25
            self.tower_range += 20
            self.attack_animation_cooldown -= 20

            return True






# Initialises and starts the starting screen
NewGame = GameStartScreen()
NewGame.run()
    
pygame.quit()
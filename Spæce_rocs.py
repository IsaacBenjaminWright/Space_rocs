import pygame
import random
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

class Food():
    def __init__(self, color, value, size):
        self.x = random.randint(25, SCREEN_WIDTH-25)
        self.y = random.randint(25, SCREEN_HEIGHT-25)
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.value = value
    def food_tuppy(self):
        return(self.x, self.y, self.width, self.height)
    def get_color(self):
        return self.color
    def get_value(self):
        return self.value

class Player():
    def __init__(self, speed, start_coordinates_size: list[int, int, int, int]):
        self.speed = speed
        self.rect = pygame.Rect(start_coordinates_size)
        self.start_coordinates_size = start_coordinates_size
        self.tails = 0
    def get_rect(self):
        return self.rect
    def get_speed(self):
        return self.speed
    def up_speed(self):
        self.speed += .5
    def reset_speed(self):
        self.speed = 2
    def get_start_x(self):
        return random.randint(25, SCREEN_WIDTH-25)
    def get_start_y(self):
        return random.randint(25, SCREEN_HEIGHT-25)
    def add_tail(self):
        self.tails += 1
    def get_tails(self):
        return self.tails
    
class Blast():
    def __init__(self, speed, start_coordinates_size: list[int, int, int, int], position):
        self.speed = speed
        self.rect = pygame.Rect(start_coordinates_size)
        self.start_coordinates_size = start_coordinates_size
        self.position = position
    def get_rect(self):
        return self.rect
    def get_speed(self):
        return self.speed
    def get_position(self):
        return self.position
    def update_x(self, sign):
        self.rect.x += (self.speed*sign)    
    def update_y(self, sign):
        self.rect.y += (self.speed*sign)    
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player(2, [300, 400, 25, 25])
player_rect = player.get_rect()
player_position = [player.get_start_x(), player.get_start_y()]

score_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 100)
game_over_score_font = pygame.font.Font(None, 60)

axis = 0
foods = []
roadblocks = []
upper = 1000


blasts = []

score = 0
player_move = 0
username = ''
level = 0
level_up_score = 20
scale_level_up = 20

coin_sound = pygame.mixer.Sound('coin.mp3')
coin2_sound = pygame.mixer.Sound('coin2.mp3')
coin3_sound = pygame.mixer.Sound('coin3.mp3')
fail_sound = pygame.mixer.Sound('fail.mp3')
start_sound = pygame.mixer.Sound('start.mp3')

def game_over():
    global score, player_move, foods, player_position, roadblocks, blasts, username, level, level_up_score, speed, upper, scale_level_up
    
    with open('high_score.txt', 'a') as file_handle:
        file_handle.write(f'{username},{score}\n')

    with open('high_score.txt', 'r') as file_handle:
        high_score = 0
        player_high_score = ''
        for line in file_handle:
            line = line.strip().split(',')
            if int(line[1]) > high_score:
                high_score = int(line[1])
                player_high_score = f'{line[0]} {line[1]}'  
    
    player_move = 0
    foods = []
    roadblocks = []
    blasts = []
    player_position = [player.get_start_x(), player.get_start_y()]
    level = 0
    level_up_score = 20
    player.reset_speed()
    upper = 1000
    scale_level_up = 20
    
    fail_sound.play()
    game_over_text = game_over_font.render(f'GAME_OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (300,400))
    score_text = game_over_score_font.render(f'SCORE: {score}', True, (255, 255, 255))
    screen.blit(score_text, (320,475))    
    pygame.display.update()
    pygame.time.delay(3000) 
    
    screen.fill((0,0,0))
    pygame.display.update()
     
    game_start_text = game_over_font.render(f'SPÆCE_ROKCS', True, (255, 255, 255))
    screen.blit(game_start_text, (300,400))
    pygame.display.update()
    start_sound.play()
    pygame.time.delay(1000)
    game_start_text = game_over_font.render(f'SPÆCE_ROKCS', True, (255, 255, 255))
    screen.blit(game_start_text, (300,400))    
    game_start_text = game_over_font.render(f'HIGH_SCORE: {player_high_score}', True, (255, 255, 255))
    screen.blit(game_start_text, (300,100))
    pygame.display.update() 
    pygame.time.delay(2000)
    score = 0

def level_up():
    global score, player_move, foods, player_position, roadblocks, blasts, username, level, upper, scale_level_up
    
    game_over_text = game_over_font.render(f'LEVEL_UP: {level}', True, (255, 255, 255))
    screen.blit(game_over_text, (300,400))    
    pygame.display.update()
    pygame.time.delay(1000) 
    
    scale_level_up += 10
    player_move = 0
    foods = []
    roadblocks = []
    blasts = []
    if upper > 2:
        upper -= 100
    
    player.up_speed()
    

input_text = game_over_font.render(f'USER_NAME:', True, (255, 255, 255))
screen.blit(input_text, (300,400))
start_sound.play()
key = pygame.key.get_pressed()
typing = True
while typing:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and typing:
            if event.key == pygame.K_RETURN:
                print("Username:", username)
                typing = False
            elif event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            else:
                username += event.unicode
            
            screen.fill((0, 0, 0))
        
            input_text = game_over_font.render(f'USER_NAME: {username}', True, (255, 255, 255))
            screen.blit(input_text, (300, 400))
         
            pygame.display.update()             

run = True
while run:

    screen.fill((0,0,0))
    
    
    if len(foods) < 3:
        random_num = random.randint(1, 8)
        golden_num = random.randint(1, 20)
        white_num = random.randint(1, 30)
        if random_num == 1:
            new_food = Food((0, 0, 255), 4, (20, 20))
            foods.append(new_food)
        elif golden_num == 1 and random_num != 1:
            new_food = Food((255, 255, 0), 12, (10, 10))
            foods.append(new_food)
        elif white_num == 1 and random_num != 1 and golden_num != 1:
            new_food = Food((255, 255, 255), 0, (8, 8))
            foods.append(new_food)
        else:
            new_food = Food((0, 255, 0), 2, (30, 30))
            foods.append(new_food)
            
    random_num = random.randint(1, upper)
    if random_num == 1 and len(roadblocks) < 50:
        new_roadblock = Food((255, 0, 0), 0, (random.randint(10, 50), random.randint(10, 50)))
        x = new_roadblock.food_tuppy()[0] - player_position[0]
        y = new_roadblock.food_tuppy()[1] - player_position[1]
        if ((x > 0 and x < 100) or (x < 0 and x > -100)) and ((y > 0 and y < 100) or (y < 0 and y > -100)):
            print('testcase')
        else:
            roadblocks.append(new_roadblock)
            
    elif random_num == 1 and len(roadblocks) >= 50:
        roadblocks.remove(roadblocks[0])
        
        new_roadblock = Food((255, 0, 0), 0, (random.randint(10, 50), random.randint(10, 50)))
        x = new_roadblock.food_tuppy()[0] - player_position[0]
        y = new_roadblock.food_tuppy()[1] - player_position[1]
        if ((x > 0 and x < 100) or (x < 0 and x > -100)) and ((y > 0 and y < 100) or (y < 0 and y > -100)):
            print('testcase')
        else:
            roadblocks.append(new_roadblock)       
        
    for roadblock in roadblocks:
        pygame.draw.rect(screen, roadblock.get_color(), roadblock.food_tuppy())
    for food in foods:
        pygame.draw.rect(screen, food.get_color(), food.food_tuppy())
    for blast in blasts:
        pygame.draw.rect(screen, (100, 100, 100), blast.get_rect())
        
    pygame.draw.rect(screen, (255, 0, 255), player.get_rect())
    
    #for tail in range(0, players.get_tails(), 1):
        
    key = pygame.key.get_pressed()

    if player.get_rect().left > 0 and player.get_rect().right < SCREEN_WIDTH and player.get_rect().top > 0 and player.get_rect().bottom < SCREEN_HEIGHT:
        if key[pygame.K_a] == True:
            player_move = -player.get_speed()
            axis = 0
            direction = 1
        if key[pygame.K_d] == True:
            player_move = player.get_speed()
            axis = 0
            direction = 2
        if key[pygame.K_w] == True:
            player_move = -player.get_speed()
            axis = 1
            direction = 3
        if key[pygame.K_s] == True:
            player_move = player.get_speed()
            axis = 1
            direction = 4
        if key[pygame.K_SPACE] == True:
            new_blast = Blast(5, [player_position[0], player_position[1], 10, 10], [player_position[0], player_position[1]])
            blasts.append(new_blast)
    else:
        game_over()
        
    for blast in blasts:
        if direction == 1:
            blast.update_x(-1)
        elif direction == 2:
            blast.update_x(1)
        elif direction == 3:
            blast.update_y(-1)
        elif direction == 4:
            blast.update_y(1)
            
    player_position[axis] += player_move 
    player_rect.x = round(player_position[0])
    player_rect.y = round(player_position[1])    
    
    for food in foods:
        if player_rect.colliderect(pygame.Rect(food.food_tuppy())):
            foods.remove(food)
            score += food.get_value()
            if food.get_value() == 0:
                num = len(roadblocks)
                roadblocks = []
                for num in range(num):
                    new_food = Food((255, 255, 255), 2, (30, 30))
                    foods.append(new_food)
                    
            if score > level_up_score:
                level_up_score += scale_level_up
                level += 1
                level_up()
            
            random_num = random.randint(1, 3)
            if random_num == 1:
                coin_sound.play()
            elif random_num == 2:
                coin2_sound.play()
            elif random_num == 3:
                coin3_sound.play()
                
    remaining_blasts = []
    remaining_roadblocks = []
    for roadblock in roadblocks:       
        if player_rect.colliderect(pygame.Rect(roadblock.food_tuppy())):
            game_over()
        did_collide = False
        remaining_blasts = []
        for blast in blasts:
            if not blast.get_rect().colliderect(pygame.Rect(roadblock.food_tuppy())):
                remaining_blasts.append(blast)
            else:
                did_collide = True
        if not did_collide:
            remaining_roadblocks.append(roadblock)
        blasts = remaining_blasts
    roadblocks = remaining_roadblocks 
        
    score_text = score_font.render(f'score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10,10))
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
    
pygame.quit()
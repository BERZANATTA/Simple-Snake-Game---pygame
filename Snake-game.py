import pygame
import sys, random
import time
from pygame.math import Vector2

class SNAKE:
  """This class represents the snake in the game."""
  def __init__(self):
    # Initialize the snake's body segments and direction
    self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
    self.direction = Vector2(0,0)
    self.new_block = False # Used to determine whether to add a new segment to the snake
    
    # Load graphics for the snake
    self.head_up = pygame.image.load('Graphics/Snake-head-up.png').convert_alpha()
    self.head_down = pygame.image.load('Graphics/Snake-head-down.png').convert_alpha()
    self.head_right = pygame.image.load('Graphics/Snake-head-right.png').convert_alpha()
    self.head_left = pygame.image.load('Graphics/Snake-head-left.png').convert_alpha()
    self.tail_up = pygame.image.load('Graphics/Snake-tail-up.png').convert_alpha()
    self.tail_down = pygame.image.load('Graphics/Snake-tail-down.png').convert_alpha()
    self.tail_right = pygame.image.load('Graphics/Snake-tail-right.png').convert_alpha()
    self.tail_left = pygame.image.load('Graphics/Snake-tail-left.png').convert_alpha()

    self.body_vertical = pygame.image.load('Graphics/Snake-body-vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('Graphics/Snake-body-horizontal.png').convert_alpha()

    self.body_P = pygame.image.load('Graphics/Snake-P.png').convert_alpha()
    self.body_q = pygame.image.load('Graphics/Snake-q.png').convert_alpha()
    self.body_L = pygame.image.load('Graphics/Snake-L.png').convert_alpha()
    self.body_J = pygame.image.load('Graphics/Snake-J.png').convert_alpha()
    
    # Sound for when the snake eats
    self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
    
  def draw_snake(self):
    """Draws the snake on the screen."""
    self.update_head_graphics()
    self.update_tail_graphics()

    
    for index, block in enumerate(self.body):
      x_pos = int(block.x * CELL_SIZE)
      y_pos = int(block.y * CELL_SIZE)
      block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
      
      if index == 0:
        SCREEN.blit(self.head, block_rect)
        
      elif index == len(self.body) - 1:
        SCREEN.blit(self.tail, block_rect)
        
      else:
        previous_block = self.body[index + 1] - block
        next_block = self.body[index - 1] - block
        
        if previous_block.x == next_block.x:
          SCREEN.blit(self.body_vertical,block_rect)
          
        elif previous_block.y == next_block.y:
          SCREEN.blit(self.body_horizontal,block_rect)
          
        else:
          if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
            SCREEN.blit(self.body_J, block_rect)
            
          elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
            SCREEN.blit(self.body_q, block_rect)
            
          elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
            SCREEN.blit(self.body_L, block_rect)
            
          elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
            SCREEN.blit(self.body_P, block_rect)
            
            
          if index > 1 and index < len(self.body) - 2:
                    next_next_block = self.body[index - 2] - block
                    if next_next_block.y == previous_block.x and next_next_block.x == previous_block.y:
                        SCREEN.blit(self.body_horizontal, block_rect)
                    elif next_next_block.x == previous_block.x and next_next_block.y == previous_block.y:
                        SCREEN.blit(self.body_vertical, block_rect)

    pygame.display.flip()  
        


      
  def update_head_graphics(self):
    head_relation = self.body[1] - self.body[0]
    if head_relation == Vector2(1,0): self.head = self.head_left
    elif head_relation == Vector2(-1,0): self.head = self.head_right
    elif head_relation == Vector2(0,1): self.head = self.head_up
    elif head_relation == Vector2(0,-1): self.head = self.head_down
  
  
  def update_tail_graphics(self):
    tail_relation = self.body[-2] - self.body[-1]
    if tail_relation == Vector2(1,0): self.tail = self.tail_left
    elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
    elif tail_relation == Vector2(0,1): self.tail = self.tail_up
    elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
  
    

  
  def move_snake(self):
    if self.new_block == True:
      body_copy = self.body[:]
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]
      self.new_block = False
      
    else:
      body_copy = self.body[:-1]
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]
      
  
    
  def add_block(self):
    self.new_block = True
    
    
  def play_crunch_sound(self):
    self.crunch_sound.play()
    
    
  def reset(self):
    """Resets the snake to its initial state. Used when restarting the game."""
    self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
    self.direction = Vector2(0,0)

      
      

class FOOD:
  """This class represents the food in the game."""
  def __init__(self):
    # Randomize the position of the food when it is first created
    self.randomize()
  
    
  def draw_food(self):
    """Draws the food on the screen."""
    food_rect = pygame.Rect(int(self.pos.x * CELL_SIZE),int(self.pos.y * CELL_SIZE),CELL_SIZE,CELL_SIZE)
    SCREEN.blit(STRAWBERRY,food_rect)
    
  def randomize(self):
    """Randomizes the position of the food on the grid."""
    self.x = random.randint(0,CELL_NUMBER-1)
    self.y = random.randint(0,CELL_NUMBER-1)
    self.pos = Vector2(self.x,self.y)
    
class MAIN:
  """Main game class that controls game updates, drawing, and logic."""
  def __init__(self):
    self.snake = SNAKE()
    self.food = FOOD()
    
  def update(self):
    """Updates the game state, including moving the snake and checking for collisions."""
    self.snake.move_snake()
    self.check_collision()
    self.check_fail()
    
  def draw_elements(self):
    self.draw_grass()
    self.food.draw_food()
    self.snake.draw_snake()
    self.draw_score()
    
  def check_collision(self):
    """Checks for a collision between the snake and food, and handles the snake growth and sound effect."""
    if self.food.pos == self.snake.body[0]:
      self.food.randomize()
      self.snake.add_block()
      self.snake.play_crunch_sound()
      
    for block in self.snake.body[1:]:
      if block == self.food.pos:
        self.food.randomize()
      
      
  def check_fail(self):
    """Checks for failure conditions, such as the snake colliding with itself or the game boundaries."""
    if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
      self.game_over()
      
    for block in self.snake.body[1:]:
      if block == self.snake.body[0]:
        self.game_over()
      
  def game_over(self):
    """Resets the game to its initial state, effectively starting over."""
    self.snake.reset()
  
  def draw_grass(self):
    """Draws the grass background on the game screen."""
    grass_color = (165,210,60)
    
    for row in range(CELL_NUMBER):
      if row % 2 == 0:
        for col in range(CELL_NUMBER):
          if col % 2 == 0:
            grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE,CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(SCREEN,grass_color,grass_rect)
      
      else:
        for col in range(CELL_NUMBER):
          if col % 2 != 0:
            grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE,CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(SCREEN,grass_color,grass_rect)
      
  def draw_score(self):
    """Displays the current score (length of the snake) on the screen."""
    score_text = str(len(self.snake.body) - 3)
    score_surface = game_font.render(score_text,True,(50,70,10))
    score_x = int(CELL_SIZE * CELL_NUMBER - 40)
    score_y = int(CELL_SIZE* CELL_NUMBER - 420)
    score_rect = score_surface.get_rect(midleft = (score_x, score_y))
    strawberry_rect = STRAWBERRY.get_rect(midright = (score_rect.left, score_rect.centery))
    bg_rect = pygame.Rect(strawberry_rect.left - 3, strawberry_rect.top - 4, strawberry_rect.width + score_rect.width + 10, strawberry_rect.height + 8)
    
    pygame.draw.rect(SCREEN,(165,210,61),bg_rect)
    SCREEN.blit(score_surface, score_rect)  
    SCREEN.blit(STRAWBERRY, strawberry_rect )
    pygame.draw.rect(SCREEN,(55,75,10),bg_rect,2)
    
  


pygame.mixer.pre_init(44100,-16,2,512) 
pygame.init()
CELL_SIZE = 30
CELL_NUMBER = 15
SCREEN = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_SIZE * CELL_NUMBER))
CLOCK = pygame.time.Clock()
BERRY = pygame.image.load('Graphics/Strawberry.png').convert_alpha()
STRAWBERRY = pygame.transform.scale(BERRY, (15,20))
game_font = pygame.font.Font('Fonts/Numans-Regular.ttf',25)

 
main_game = MAIN()
 
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)
 


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    if event.type == SCREEN_UPDATE:
      main_game.update()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        if main_game.snake.direction.y != 1:
          main_game.snake.direction = Vector2(0,-1)
      if event.key == pygame.K_DOWN:
        if main_game.snake.direction.y != -1:
          main_game.snake.direction = Vector2(0,1)
      if event.key == pygame.K_RIGHT:
        if main_game.snake.direction.x != -1:
          main_game.snake.direction = Vector2(1,0)
      if event.key == pygame.K_LEFT:
        if main_game.snake.direction.x != 1:
          main_game.snake.direction = Vector2(-1,0)
      

    
      
  SCREEN.fill((175,215,70))
  main_game.draw_elements() 
  pygame.display.update()
  CLOCK.tick(60)
   
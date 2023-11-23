import pygame

class Player(pygame.sprite.Sprite):
  def __init__(self,pos,jump_speed):
    super().__init__()
    self.image = pygame.image.load("player.png")
    self.rect = self.image.get_rect(topleft = pos)
    
    # player movement
    self.direction = pygame.math.Vector2(0,0)
    self.gravity = 0.7
    self.jump_speed = jump_speed
    self.jump_number = 2
    self.jump_button_released = True
  
  def get_input(self):
    self.shift_pressed = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      self.direction.x = 1
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
      self.direction.x = -1
    else:
      self.direction.x = 0
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
      self.shift_pressed = True
    if not (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]):
      self.jump_button_released = True
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.jump_number > 0 and self.jump_button_released:
      self.jump()
      self.jump_number -= 1
      self.jump_button_released = False

  def apply_gravity(self):
    self.direction.y += self.gravity
    self.rect.y += self.direction.y

  def jump(self):
    self.direction.y = self.jump_speed

  def update(self):
    self.get_input()
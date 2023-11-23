import pygame
import tensorflow as tf
from tiles import Tile
from settings import tile_size, screen_width, final_level
from player import Player
from endpoint import EndPoint
from spikes import Spike
import random

pygame.font.init()
one_step_reloaded = tf.saved_model.load('one_step')
chooseCharacterFont = pygame.font.SysFont(None, 72)
characterDescriptionFont = pygame.font.SysFont(None, 36)
chooseCharacterText = chooseCharacterFont.render("Choose Your Character:", True, "black")
standardButton = pygame.image.load("button_standard.png")
runnerButton = pygame.image.load("button_runner.png")
jumperButton = pygame.image.load("button_jumper.png")
standardButtonHover = pygame.image.load("button_standard_hover.png")
runnerButtonHover = pygame.image.load("button_runner_hover.png")
jumperButtonHover = pygame.image.load("button_jumper_hover.png")

def ai_generate_level():
  while True:
    longest_string_length = 0
    space = 0
    empty_column = 0
    states = None
    next_char = tf.constant(['  '])
    result = [next_char]
    level_size = random.randint(150, 350)
    for i in range(level_size):
      next_char, states = one_step_reloaded.generate_one_step(next_char, states=states)
      result.append(next_char)
    ai_level_data = str(tf.strings.join(result)[0].numpy())
    if level_size >= 300:
      place_holder = [" ", " "]
    elif level_size >= 200:
      place_holder = [" ", " ", " "]
    else:
      place_holder = [" ", " ", " ", " "]
    if "P" in ai_level_data and "E" in ai_level_data:
      processed_level_data = ai_level_data.replace("b'","")
      processed_level_data = processed_level_data.split("\\r\\n")
      processed_level_data = processed_level_data + [" "]
      for index in range (len(processed_level_data)):
        if "P" in processed_level_data[index]:
          list_index = index
      string_index = processed_level_data[list_index].index("P")
      processed_level_data[list_index+1] = processed_level_data[list_index+1][:string_index-1] + "XXX" + processed_level_data[list_index+1][string_index+2:]
      for string in processed_level_data:
        if len(string) > longest_string_length:
            longest_string_length = len(string)  
      for string_index, string in enumerate(processed_level_data):
        if len(string) < longest_string_length:
            for i in range(longest_string_length - len(string)):
                processed_level_data[string_index] += " "  
      for column_index in range(longest_string_length):
        for string in processed_level_data:
            if string[column_index] == "E":
                endpoint_column_index = column_index
      for column_index in range(endpoint_column_index):
          for string in processed_level_data:
              if string[column_index] != "X":
                  space += 1
          if space == len(processed_level_data):
              empty_column += 1
          space = 0
      if empty_column > 8:
          continue
      processed_level_data = place_holder + processed_level_data
      return processed_level_data
    
class Level:
  def __init__(self,surface):
    # level setup
    self.display_surface = surface
    self.level_number_font = pygame.font.SysFont(None, 48)
    gameover_font_big = pygame.font.Font("RussoOne-Regular.ttf", 80)
    self.gameover_text_big = gameover_font_big.render("Game Over", True, (255,255,255))
    gameover_font_small = pygame.font.SysFont(None, 24)
    self.gameover_text_small = gameover_font_small.render("Press R to Restart or ESC to go back to Menu", True, (255,255,255))
    self.level_number = 1
    self.world_shift = 0
    self.gameover = True
    self.touched_spike = False
    self.switch_background = False
    self.high_score = 1
    
  def setup_level(self, layout):
    self.tiles = pygame.sprite.Group()
    self.player = pygame.sprite.GroupSingle()
    self.endpoint = pygame.sprite.Group()
    self.spikes = pygame.sprite.Group()

    for row_number,row in enumerate(layout):
      for col_number,cell in enumerate(row):
        x = col_number * tile_size
        y = row_number * tile_size
        if cell == "X":
          tile = Tile((x,y))
          if self.level_number >= 60:
            if self.level_number == 101:
              if row_number == 11:
                tile.image = pygame.image.load("rockBlock.png")
              else:
                tile.image = pygame.image.load("colourBlock.png")
            else:
              tile.image = pygame.image.load("rockBlock.png")
          else:
            tile.image = pygame.image.load("grassBlock.png")          
          self.tiles.add(tile)
        elif cell == "P":
          player_sprite = Player((x,y), self.jump_speed)
          self.player.add(player_sprite)
        elif cell == "E":
          endpoint = EndPoint((x,y-64))
          if self.level_number == 101:
            self.trophy_number = random.randint(1, 6)
            endpoint.image = pygame.image.load(f"trophy{self.trophy_number}.png")
          else:
            endpoint.image = pygame.image.load("portal.png")
          self.endpoint.add(endpoint)
        elif cell == "S":
          spike = Spike((x,y))
          self.spikes.add(spike)

  def scroll_x(self):
    player = self.player.sprite
    player_x = player.rect.centerx
    direction_x = player.direction.x
    
    if player_x < 0.2 * screen_width and direction_x < 0:
      if player.shift_pressed:
        self.world_shift = self.run_speed
        self.player_run_speed = 0
      else:
        self.world_shift = self.speed
        self.player_speed = 0
    elif player_x > 0.7 * screen_width and direction_x > 0:
      if player.shift_pressed:
        self.world_shift = -self.run_speed
        self.player_run_speed = 0
      else:
        self.world_shift = -self.speed
        self.player_speed = 0
    else:
      self.world_shift = 0
      self.player_speed, self.player_run_speed = self.speed, self.run_speed

  def horizontal_movement_collision(self):
    player = self.player.sprite
    if player.shift_pressed:
      player.rect.x += player.direction.x * self.player_run_speed
    else:
      player.rect.x += player.direction.x * self.player_speed

    for sprite in self.tiles.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.x < 0:
          player.rect.left = sprite.rect.right
        elif player.direction.x > 0:
          player.rect.right = sprite.rect.left

  def vertical_collision(self):
    player = self.player.sprite
    player.apply_gravity()

    for sprite in self.tiles.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.y < 0:
          player.rect.top = sprite.rect.bottom
          player.direction.y = 0
        elif player.direction.y > 0:
          player.rect.bottom = sprite.rect.top
          player.direction.y = 0
          player.jump_number = 2

  def clear_screen(self):
    for sprite in self.endpoint.sprites():
      if sprite.rect.colliderect(self.player.sprite.rect):
        sprite.kill()
        for sprite in self.tiles.sprites():
          sprite.kill()
        self.draw_next_level()

  def draw_next_level(self):
    self.level_number += 1
    if self.level_number % 5 == 0:
      if self.level_number == 100:
        pygame.mixer.music.load("backgroundMusic14.mp3")
        pygame.mixer.music.play(-1, 40)
      elif self.level_number >= 60:
        music_number = random.randint(4,13)
        pygame.mixer.music.load(f"backgroundMusic{music_number}.mp3")
        pygame.mixer.music.play(-1)
      else:
        music_number = random.randint(1,3)
        pygame.mixer.music.load(f"backgroundMusic{music_number}.mp3")
        pygame.mixer.music.play(-1)
      self.switch_background = True
    if self.level_number == 101:
      pygame.mixer.music.load("backgroundMusic15.mp3")
      pygame.mixer.music.play(-1)
      self.switch_background = True
      self.setup_level(final_level)
    elif self.level_number <= 100:
      self.setup_level(ai_generate_level())

  def display_level_number(self):
    if self.level_number <= 100:
      self.level_number_text = self.level_number_font.render(f"Level {self.level_number}", True, (255,0,0))
      self.display_surface.blit(self.level_number_text, (50, 50))

  def player_spike_collision(self):
    for sprite in self.spikes.sprites():
      if sprite.rect.colliderect(self.player.sprite.rect):
        self.touched_spike = True

  def game_over(self):
    keys = pygame.key.get_pressed()
    player_y = self.player.sprite.rect.centery
    reset_background = False
    if self.level_number == 102:
      self.high_score = "100% Game Complete!"
      self.level_number = 1
      for sprite in self.tiles.sprites():
        sprite.kill()
      self.setup_level(ai_generate_level())
      return False, False, False, True
    if (player_y > 1100 or self.touched_spike) and self.gameover:
      self.player.sprite.jump_number = 0
      self.display_surface.fill("black")
      self.display_surface.blit(self.gameover_text_big, (552, 50))
      self.display_surface.blit(self.gameover_text_small, (596, 140))
      if keys[pygame.K_r] or keys[pygame.K_ESCAPE]:
        if self.level_number >= 60:
          music_number = random.randint(1,3)
          pygame.mixer.music.load(f"backgroundMusic{music_number}.mp3")
          pygame.mixer.music.play(-1)
          reset_background = True
        if self.level_number > self.high_score:
          self.high_score = self.level_number
        self.level_number = 1
        self.gameover = False
        self.touched_spike = False
        for sprite in self.tiles.sprites():
          sprite.kill()
        self.setup_level(ai_generate_level())
        self.gameover = True
        if keys[pygame.K_ESCAPE]:
          return False, True, reset_background, False
    return True, False, reset_background, False

  def chooseCharacter(self):
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if (mouse[0] >= 642 and mouse[0] <= 879) and (mouse[1] >= 220 and mouse[1] <= 289):
          self.jump_speed = -17
          self.speed, self.run_speed = 4, 6
          return False
        if (mouse[0] >= 363 and mouse[0] <= 567) and (mouse[1] >= 220 and mouse[1] <= 289):
          self.jump_speed = -14
          self.speed, self.run_speed = 6, 9
          return False
        if (mouse[0] >= 954 and mouse[0] <= 1158) and (mouse[1] >= 220 and mouse[1] <= 289):
          self.jump_speed = -20.6
          self.speed, self.run_speed = 3, 4
          return False
    self.display_surface.fill("white")
    self.display_surface.blit(chooseCharacterText, (chooseCharacterText.get_rect(center=(screen_width/2, 130))))
    characterDescription = ""
    if (mouse[0] >= 642 and mouse[0] <= 879) and (mouse[1] >= 220 and mouse[1] <= 289):
      self.display_surface.blit(standardButtonHover, (642, 220))
      characterDescription = "Standard Movement Speed     Standard Jumping Height"
    else:
      self.display_surface.blit(standardButton, (642, 220))
    if (mouse[0] >= 363 and mouse[0] <= 567) and (mouse[1] >= 220 and mouse[1] <= 289):
      self.display_surface.blit(runnerButtonHover, (363, 220))
      characterDescription = "50% Faster Movement Speed     33% Lower Jumping Height"
    else:
      self.display_surface.blit(runnerButton, (363, 220))
    if (mouse[0] >= 954 and mouse[0] <= 1158) and (mouse[1] >= 220 and mouse[1] <= 289):
      self.display_surface.blit(jumperButtonHover, (954, 220))
      characterDescription = "50% Higher Jumping Height     33% Slower Running Speed"
    else:
      self.display_surface.blit(jumperButton, (954, 220))
    characterDescriptionText = characterDescriptionFont.render(characterDescription, True, "black")
    self.display_surface.blit(characterDescriptionText, (characterDescriptionText.get_rect(center=(screen_width/2, 350))))
    return True

  def run(self):
    # draws level tiles
    self.tiles.update(self.world_shift)
    self.tiles.draw(self.display_surface)
    self.endpoint.update(self.world_shift)
    self.endpoint.draw(self.display_surface)
    self.spikes.update(self.world_shift)
    self.spikes.draw(self.display_surface)
    self.display_level_number()
    self.scroll_x()

    # draws the player
    self.player.update()
    self.horizontal_movement_collision()
    self.vertical_collision()
    self.clear_screen()
    self.player_spike_collision()
    self.player.draw(self.display_surface)
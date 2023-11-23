import pygame

class Tile(pygame.sprite.Sprite):
  def __init__(self,pos):
    super().__init__()
    self.image = pygame.image.load("grassBlock.png")
    self.rect = self.image.get_rect(topleft = pos)

  def update(self,x_shift):
    self.rect.x += x_shift
  
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (136,136,136)
BACKGROUND = (0, 255, 255)
#background and other images
background=pygame.image.load('fondo.png')
mario=pygame.image.load('zelda.png')
#set size of mario
mario = pygame.transform.scale(mario, (150, 150))



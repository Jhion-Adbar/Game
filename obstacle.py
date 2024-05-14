import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))


shape = [                   # ano list of string and size
'  xxx        x        xxx',
'  xxxx      xxx      xxxx',
'  xxxxxxxxxxxxxxxxxxxxxxx',
'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
'  xxxxxxxxxxxxxxxxxxxxxxx',
'      xxxxxxxxxxxxxxx',              # this shape is creat by sprite
'       xxxx     xxxx',
'        xx       xx',]


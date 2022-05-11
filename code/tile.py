import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((30,30))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - 64))
        else:
            self.rect = self.image.get_rect(topleft = pos)
            self.hitbox = self.rect.inflate(0,-10)
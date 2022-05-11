import pygame
from network import Network
from tile import Tile
from player import Player
from p import P
from debug import debug
from support import *
from random import choice
from weapon import Weapon


class Level:
    def __init__(self,network):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        # gathering

        #grass
        self.destroyed_grass = 0
        self.font = pygame.font.Font('graphics/font/joystix.ttf', 21)
        self.text_grass = self.font.render(str(self.destroyed_grass), True, 'white')
        self.text_grass_rect = self.text_grass.get_rect()
        self.text_grass_rect.center = (100, 100)
        self.grass_image = pygame.image.load('graphics/plantas/grass_1.png')
        self.grass_image_rect = self.grass_image.get_rect()
        self.grass_image_rect.center = (40, 100)

        #stones
        self.destroyed_stones = 0
        self.text_stones = self.font.render(str(self.destroyed_grass), True, 'white')
        self.text_stones_rect = self.text_stones.get_rect()
        self.text_stones_rect.center = (100, 200)
        self.stone_image = pygame.image.load('graphics/pedras/pedra.png')
        self.stone_image_rect = self.stone_image.get_rect()
        self.stone_image_rect.center = (40, 200)

        #trees
        self.destroyed_trees = 0
        self.text_trees = self.font.render(str(self.destroyed_grass), True, 'white')
        self.text_trees_rect = self.text_trees.get_rect()
        self.text_trees_rect.center = (100, 300)
        self.tree_image = pygame.image.load('graphics/arvores/arvores.png')
        self.tree_image_rect = self.stone_image.get_rect()
        self.tree_image_rect.center = (40, 300)

        # sprite setup
        self.create_map(network)

    def create_map(self,network):
        layout = {
            'boundary': import_csv_layout("map/delimitacao.csv"),
            'plantas': import_csv_layout('map/plantas.csv'),
            'pedras': import_csv_layout('map/pedras.csv'),
            'arvores': import_csv_layout('map/arvores.csv'),
            'moveis': import_csv_layout('map/moveis.csv'),
            'agua': import_csv_layout('map/agua.csv'),
        }
        graphics = {
            'plantas': import_folder('graphics/plantas'),
            'pedras': import_folder('graphics/pedras'),
            'arvores': import_folder('graphics/arvores')
        }
        for style, layout in layout.items():
            for fila_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * 30
                        y = fila_index * 30
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                if style == 'moveis':
                    Tile((x, y), [self.obstacle_sprites], 'invisible')       
                if style == 'plantas':
                    random_plantas_image = choice(graphics['plantas'])
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites,self.attackable_sprites], 'plantas', random_plantas_image)
                if style == 'pedras':
                    random_pedras_image = choice(graphics['pedras'])
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites,self.attackable_sprites], 'pedras', random_pedras_image)
                if style == 'arvores':
                    random_arvores_image = choice(graphics['arvores'])
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites,self.attackable_sprites], 'arvores', random_arvores_image)


        self.player = Player((1500, 1000), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, network)
        self.p = P([self.visible_sprites],self.obstacle_sprites, self.create_attack, self.destroy_attack,self.destroy_attack_p,self.create_attack_p,network)
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def create_attack_p(self):
        self.current_attack_p = Weapon(self.p,[self.visible_sprites, self.attack_sprites])
	
    def destroy_attack_p(self):
        if self.current_attack_p:
            self.current_attack_p.kill()
        self.current_attack_p = None

    def gathering_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'plantas':
                            target_sprite.kill()
                            self.destroyed_grass += 1
                            self.font = pygame.font.Font('graphics/font/joystix.ttf', 21)
                            self.text_grass = self.font.render(
                                'x' + str(self.destroyed_grass), True, 'white')
                            self.text_grass_rect = self.text_grass.get_rect()
                            self.text_grass_rect.center = (100, 100)
                        elif target_sprite.sprite_type == 'pedras':
                            target_sprite.kill()
                            self.destroyed_stones += 1
                            self.font = pygame.font.Font('graphics/font/joystix.ttf', 21)
                            self.text_stones = self.font.render(
                                'x' + str(self.destroyed_stones), True, 'white')
                            self.text_stones_rect = self.text_stones.get_rect()
                            self.text_stones_rect.center = (100, 200)
                        elif target_sprite.sprite_type == 'arvores':
                            target_sprite.kill()
                            self.destroyed_trees += 1
                            self.font = pygame.font.Font('graphics/font/joystix.ttf', 21)
                            self.text_trees = self.font.render(
                                'x' + str(self.destroyed_trees), True, 'white')
                            self.text_trees_rect = self.text_trees.get_rect()
                            self.text_trees_rect.center = (100, 300)

        self.display_surface.blit(self.text_grass, self.text_grass_rect)
        self.display_surface.blit(self.grass_image, self.grass_image_rect)

        self.display_surface.blit(self.text_stones, self.text_stones_rect)
        self.display_surface.blit(self.stone_image, self.stone_image_rect)

        self.display_surface.blit(self.text_trees, self.text_trees_rect)
        self.display_surface.blit(self.tree_image, self.tree_image_rect)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.p)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.gathering_logic()
        recv = self.player.send_data()
        if recv != None:	
            self.p.recv_data(recv)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

#!/usr/bin/env python3
# coding:utf-8
import pygame
import pytmx
import pyscroll
from player import Player


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygamon")

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # générer un joueur
        player_position = tmx_data.get_object_by_id(1)
        self.player = Player(player_position.x, player_position.y)

        # liste de collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le goupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        # rect de collision pour entrer dans house1
        enter_house1 = tmx_data.get_object_by_name("enter_house1")
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        self.map = "world"
    
    def hundle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.change_animation("up")
            self.player.move_up()
        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.player.change_animation("down")
            self.player.move_down()
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.change_animation("right")
            self.player.move_right()
        elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.change_animation("left")
            self.player.move_left()
    
    def switch_house(self):
         # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("house1.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste de collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le goupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        # rect de collision pour sortir de house1
        exit_house1 = tmx_data.get_object_by_name("exit")
        self.exit_house1_rect = pygame.Rect(exit_house1.x, exit_house1.y, exit_house1.width, exit_house1.height)

        # récup pt de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house1')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20
    
    def switch_world(self):
         # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste de collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le goupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        # rect de collision pour entrer dans house1
        enter_house1 = tmx_data.get_object_by_name("enter_house1")
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        # récup pt de spawn devant la maison
        exit_spawn_house_point = tmx_data.get_object_by_name('exit_house1')
        self.player.position[0] = exit_spawn_house_point.x
        self.player.position[1] = exit_spawn_house_point.y + 20

    def update(self):
        self.group.update()

        # vérif entrée maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_house1_rect):
            self.switch_house()
            self.map = "house1"
        if self.map == "house1" and self.player.feet.colliderect(self.exit_house1_rect):
            self.switch_world()
            self.map = "world"

        # vérif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            self.player.save_location()
            self.hundle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)
        
        pygame.quit()
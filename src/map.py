#!/usr/bin/env python3
# coding:utf-8
from dataclasses import dataclass
import pygame
import pyscroll
import pytmx

from src.dialog import DialogBox
from src.entity import NPC, Entity


@dataclass
class Portal:
    origin_world: str
    origin_point: str | int
    target_world: str
    target_point: str | int


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    NPCs: list[NPC]


class MapManager:
    def __init__(self, screen: pygame.Surface, player: Entity):
        self.maps = {}
        self.map_layer = None
        self.current_map = "world"
        self.player = player
        self.register_map("world", screen, player, portals=[
            Portal(
                origin_world='world',
                origin_point='enter_house',
                target_world='house',
                target_point='spawn'
            ),
            Portal(
                origin_world='world',
                origin_point='enter_house2',
                target_world='house2',
                target_point='spawn'
            ),
            Portal(
                origin_world='world',
                origin_point='enter_dungeon',
                target_world='dungeon',
                target_point='spawn'
            )
        ], npcs=[
            NPC("paul", nb_points=4, dialog=[
                "Bonjour jeune aventurier !",
                "Le temps est beau aujourd'hui.",
                "Pourrais-tu aller me chercher quelques diamants dans le donjon ?",
                "Merci, je te revaudrai ça."
            ]),
            NPC("robin", nb_points=2, dialog=["Bonjour ! Comment va-tu ?"])
        ])
        self.register_map("house", screen, player, portals=[
            Portal(
                origin_world='house',
                origin_point='exit',
                target_world='world',
                target_point='exit_house'
            )
        ])
        self.register_map("house2", screen, player, portals=[
            Portal(
                origin_world='house2',
                origin_point='exit',
                target_world='world',
                target_point='exit_house2'
            )
        ])
        self.register_map("dungeon", screen, player, portals=[
            Portal(
                origin_world='dungeon',
                origin_point='exit',
                target_world='world',
                target_point='exit_dungeon'
            )
        ], npcs=[
            NPC("boss", nb_points=4, dialog=["Mwahaha... !", "Je garde ces lieux... !"])
        ])
        self.teleport_player("Player")
        self.teleport_npcs()

    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.origin_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    # copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(portal.target_point)

        # collisions
        for sprite in self.get_sprites():

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
                sprite.speed = 0
            else:
                sprite.speed = sprite.default_speed

            if type(sprite) == NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = sprite.default_speed

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, screen: pygame.Surface, player: Entity, portals: list[Portal] = None,
                     npcs: list[NPC] = None):
        if portals is None:
            portals = []
        if npcs is None:
            npcs = []
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
        self.map_layer.zoom = 2

        # liste de collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=5)
        group.add(player)

        for npc in npcs:
            group.add(npc)

        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def change_screen_size(self, screen: pygame.Surface):
        # puisqu'on peut changer la taille de la fenêtre il faut mettre à jour la taille du map layer
        self.map_layer.set_size(screen.get_size())
        self.update()
        self.draw(screen)

    def get_map(self) -> Map: return self.maps[self.current_map]

    def get_group(self) -> pyscroll.PyscrollGroup: return self.get_map().group
    def get_grp(self) -> pyscroll.PyscrollGroup: return self.get_group()
    def get_sprites(self) -> list[Entity]: return self.get_grp().sprites()

    def get_walls(self) -> list[pygame.Rect]: return self.get_map().walls

    def get_object(self, *args):
        if isinstance(args[0], str):
            return self.get_map().tmx_data.get_object_by_name(args[0])
        else:
            return self.get_map().tmx_data.get_object_by_id(args[0])

    def teleport_npcs(self):
        for map_ in self.maps:
            map_data = self.maps[map_]
            npcs = map_data.NPCs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self, screen: pygame.Surface):
        self.get_grp().draw(screen)
        self.get_grp().center(self.player.rect.center)

    def update(self):
        self.get_grp().update()
        self.check_collisions()

        for npc in self.get_map().NPCs:
            npc.move()

    def check_npc_collisions(self, dialog_box: DialogBox) -> bool:
        for sprite in self.get_sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)
                return True
        return False

    def check_sign_collisions(self, dialog_box: DialogBox) -> bool:
        for obj in self.get_map().tmx_data.objects:
            if obj.name == 'sign' and pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(self.player.rect):
                dialog_box.execute(["Parlez aux PNJ en appuyant sur espace.", "Partez visiter les maisons !",
                                    "Aventurez-vous dans le donjon, mais prenez garde au boss !"])
                return True
        return False

#!/usr/bin/env python3
# coding:utf-8
import pygame
from pygame import locals

from src.dialog import DialogBox
from src.player import Player
from src.map import MapManager as MapMgr


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600), locals.RESIZABLE)
        pygame.display.set_caption("Pygamon")

        # générer un joueur
        self.player = Player()
        self.map_mgr = MapMgr(self.screen, self.player)
        self.dialog_box = DialogBox(self.screen)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.move_left()

    def update(self):
        self.map_mgr.update()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_mgr.draw(self.screen)
            self.dialog_box.render(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_SPACE:
                                self.map_mgr.check_npc_collisions(self.dialog_box)
                    case locals.VIDEORESIZE:
                        width, height = event.size
                        if width < 800:
                            width = 800
                        if height < 600:
                            height = 600
                        self.screen = pygame.display.set_mode((width, height), locals.RESIZABLE)
                        self.map_mgr.change_screen_size(self.screen)
                        self.dialog_box.change_screen_size(self.screen)

            clock.tick(60)

        pygame.quit()

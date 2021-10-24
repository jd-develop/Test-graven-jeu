#!/usr/bin/env python3
# coding:utf-8
import pygame


class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.sprite_sheet = pygame.image.load(f"sprites/{name}.png")
        self.animation_index = 0
        self.clock = 0
        self.images = {
            "down": self.get_images(0),
            "left": self.get_images(32),
            "right": self.get_images(64),
            "up": self.get_images(96)
        }
        self.speed = 2
        self.default_speed = self.speed

    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        if self.name == 'player':
            self.image.set_colorkey([255, 0, 255])
        else:
            self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed * 8

        if self.clock >= 100:

            self.animation_index += 1
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

    def get_images(self, y):
        images = []

        for i in range(0, 3):
            x = i * 32
            images.append(self.get_image(x, y))

        return images

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        if self.name == 'player':
            image.set_colorkey([255, 0, 255])
        else:
            image.set_colorkey([0, 0, 0])
        return image
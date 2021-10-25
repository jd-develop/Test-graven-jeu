#!/usr/bin/env python3
# coding:utf-8
import pygame
import math


class DialogBox:

    X_POS = 10

    def __init__(self, screen: pygame.Surface):
        self.box = pygame.image.load('dialogs/dialog_box.png')
        self.width = math.ceil(screen.get_width() - screen.get_width() / 100)
        self.height = math.ceil(self.width*100 / 700)
        self.box = pygame.transform.scale(self.box, (
            self.width,
            self.height)
                                          )
        self.y_pos = screen.get_height() - self.height - 10
        self.texts = ["Bonjour ! Comment ça va ?"]
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("dialogs/dialog_font.ttf", 18)
        self.reading = False

    def execute(self, dialog: list[str] = None):
        if dialog is None:
            dialog = ["Bonjour ! Comment ça va ?"]
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def render(self, screen: pygame.Surface):
        if self.reading:
            self.letter_index += 1

            screen.blit(self.box, (self.X_POS, self.y_pos))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POS + 60, self.y_pos + 40))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False

    def change_screen_size(self, screen: pygame.Surface):
        self.y_pos = screen.get_height() - self.height - 10

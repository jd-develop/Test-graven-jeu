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
        self.texts = ["Bonjour ! Allez lire le panneau en appuyant sur espace."]
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("dialogs/dialog_font.ttf", 18)
        self.reading = True

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
            if len(self.texts[self.text_index][0:self.letter_index]) < 57:
                text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
                text2 = ""
                multiline = False
            else:
                sentence = (self.texts[self.text_index][0:self.letter_index]).split()
                text_to_render = ""
                word_number = 0
                for e, word in enumerate(sentence):
                    word_number = e
                    text_to_render += word + " "
                    if len(text_to_render) >= 53:
                        break
                text2 = ""
                for word in sentence[word_number + 1:len(sentence)]:
                    text2 += word + " "
                text = self.font.render(text_to_render, False, (0, 0, 0))
                text2 = self.font.render(text2, False, (0, 0, 0))
                multiline = True
            if not multiline:
                screen.blit(text, (self.X_POS + 50, self.y_pos + 40))
            else:
                screen.blit(text, (self.X_POS + 50, self.y_pos + 30))
                screen.blit(text2, (self.X_POS + 50, self.y_pos + 50))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False

    def change_screen_size(self, screen: pygame.Surface):
        self.y_pos = screen.get_height() - self.height - 10

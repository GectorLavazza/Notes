import pygame
from pygame import font

from settings import *
from datetime import datetime


class Ui:
    def __init__(self, screen):
        self.screen = screen


class Text(Ui):
    def __init__(self, screen, font_size, pos, center_align=False, right_align=False, bottom_align=False,
                 vertical_center_align=False):
        super().__init__(screen)
        self.font = font.Font(PATH + 'fonts/PixelOperatorMono8.ttf', font_size)

        self.center_align = center_align
        self.right_align = right_align
        self.bottom_align = bottom_align
        self.vertical_center_align = vertical_center_align

        self.color = WHITE

        self.pos = pos

        self.render = self.font.render('', True, self.color)

        self.prev = ''

        self.surface = pygame.Surface(self.render.size, pygame.SRCALPHA)

        self.surface_width = self.surface.width

    def update(self, message, dt):
        if message != self.prev:
            self.surface_width = self.surface.width

            self.render = self.font.render(str(message), True,
                                           self.color)

        x, y = self.pos
        if self.center_align:
            x = self.pos[0] - self.render.width // 2
        if self.vertical_center_align:
            y = self.pos[1] - self.render.height // 2
        if self.right_align:
            x = self.pos[0] - self.render.width
        if self.bottom_align:
            y = self.pos[1] - self.render.height

        w, h = self.render.size
        # self.surface_width += dt * 10
        # self.surface = pygame.Surface((min(w, self.surface_width), h), pygame.SRCALPHA)
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)

        self.surface.blit(self.render)
        self.screen.blit(self.surface, (x, y))

        self.prev = message


class Editor(Ui):
    def __init__(self, screen, font_size, pos=(0, 0), unit_pos=False):
        super().__init__(screen)

        self.color = WHITE
        self.font_size = font_size
        self.font = font.Font(PATH + 'fonts/PixelOperatorMono8.ttf', font_size)
        self.unit_width = self.font.render('a', True, self.color).width
        self.unit_height = self.font.render('a', True, self.color).height

        x, y = pos[0] * self.unit_width ** int(unit_pos), pos[1] * self.unit_height ** int(unit_pos)
        self.pos = x, y
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.lines = ['']
        self.lines_objects = [Text(self.surface, self.font_size, (self.pos[0], self.pos[1]))]
        self.current_line = 0
        self.current_symbol = 0

        self.tab = ' ' * 4

        self.cursor = pygame.Surface((4, self.unit_height))
        self.cursor.fill(WHITE)

        self.cursor_tick = 0
        self.cursor_visible = True

        self.current_file = 'my_note'

        self.save_tick = 0

    def add(self, symbol):
        self.cursor_visible = True
        self.cursor_tick = 0
        line = self.lines[self.current_line]
        self.lines[self.current_line] = line[:self.current_symbol] + symbol + line[
                                                                              self.current_symbol + len(symbol) - 1:]
        self.current_symbol += len(symbol)

    def new_line(self):
        if self.current_symbol < len(self.lines[self.current_line]):
            first, last = self.lines[self.current_line][:self.current_symbol], self.lines[self.current_line][
                                                                               self.current_symbol:]
            self.lines[self.current_line] = first
            self.break_line(last)
        else:
            self.break_line()
        self.current_symbol = 0

    def break_line(self, msg=''):
        self.current_line += 1
        self.lines.insert(self.current_line, msg)
        text = Text(self.surface, self.font_size,
                    (self.pos[0], self.current_line * self.unit_height * 1.5 + self.pos[1]))
        self.lines_objects.insert(self.current_line, text)
        for i in range(self.current_line + 1, len(self.lines_objects)):
            self.lines_objects[i].pos = (self.pos[0], self.pos[1] + i * self.unit_height * 1.5)

    def delete(self, word=False, line=False):
        self.cursor_visible = True
        self.cursor_tick = 0
        if self.current_symbol > 0:
            self.lines[self.current_line] = (self.lines[self.current_line][:self.current_symbol-1] +
                                             self.lines[self.current_line][self.current_symbol:])
            self.current_symbol -= 1
        else:
            if self.current_line > 0:
                self.current_line -= 1
                self.current_symbol = len(self.lines[self.current_line])
                self.lines[self.current_line] += self.lines[self.current_line + 1]
                self.lines = self.lines[:self.current_line + 1] + self.lines[self.current_line + 2:]

    def update(self, dt):
        self.surface.fill((0, 0, 0, 0))

        for i in range(len(self.lines)):
            line = self.lines[i]
            self.lines_objects[i].update(line, dt)

        self.save_tick += dt
        if self.save_tick >= 60 * 10:
            self.save_tick = 0
            self.save()

        self.cursor_tick += dt
        if self.cursor_tick >= 30:
            self.cursor_tick = 0
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            self.surface.blit(self.cursor, (self.pos[0] + self.current_symbol * self.unit_width,
                                           self.pos[1] + self.current_line * self.unit_height * 1.5))

        self.screen.blit(self.surface)

    def open(self, filename):
        self.current_file = filename

        with open(filename + '.txt') as f:
            data = [s[:-1] for s in f]

            self.lines.clear()

            for i in range(len(data)):
                self.lines.append(data[i])
                text = Text(self.surface, self.font_size,
                            (self.pos[0], (i + 1) * self.unit_height * 1.5 + self.pos[1]))
                self.lines_objects.append(text)

            self.current_symbol = len(self.lines[-1])
            self.current_line = len(self.lines) - 1

    def save(self):
        with open(self.current_file + '.txt', 'w') as f:
            for line in self.lines:
                f.write(line + '\n')


class StatusBar(Ui):
    def __init__(self, screen, editor):
        super().__init__(screen)
        self.editor = editor
        self.surface = pygame.Surface((WIDTH, self.editor.unit_width * 1.5))
        self.surface.fill(DARKEST_BLACK)
        self.pos = 0, HEIGHT - self.surface.height
        self.cursor = Text(self.screen, 16, (WIDTH - self.editor.unit_width * 0.5, HEIGHT - 1), bottom_align=True,
                           right_align=True)

    def update(self, dt):
        self.screen.blit(self.surface, self.pos)
        self.cursor.update(f'{self.editor.current_line + 1}:{self.editor.current_symbol + 1} |'
                           f' {len("".join(self.editor.lines))} chars', dt)

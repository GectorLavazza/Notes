from sys import exit
from time import time

import pygame

from load_image import load_image
from settings import *
from ui import *


def main():
    pygame.init()

    pygame.event.set_allowed(
        [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
         pygame.MOUSEBUTTONUP])

    flags = pygame.DOUBLEBUF | pygame.SCALED
    screen = pygame.display.set_mode(screen_size, flags, depth=8, vsync=1)
    pygame.display.set_caption('Notes')
    pygame.display.set_icon(load_image('logo'))

    running = 1
    clock = pygame.time.Clock()

    last_time = time()

    editor = Editor(screen, EDITOR_FONT_SIZE, (1, 1), unit_pos=True)
    status_bar = StatusBar(screen, editor)

    backspace_tick = 0
    backspace_pressed = False
    backspace_pressed_tick = 0

    while running:
        dt = time() - last_time
        dt *= 60
        last_time = time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_F10:
                    pygame.display.toggle_fullscreen()

                elif event.key == pygame.K_BACKSPACE:
                    editor.delete()
                    backspace_pressed = True

                elif event.key == pygame.K_LEFT:
                    editor.cursor_visible = True
                    editor.cursor_tick = 0

                    editor.current_symbol -= 1
                    if editor.current_symbol < 0:
                        if editor.current_line > 0:
                            editor.current_line -= 1
                            editor.current_symbol = len(editor.lines[editor.current_line])
                        else:
                            editor.current_symbol = 0

                elif event.key == pygame.K_RIGHT:
                    editor.cursor_visible = True
                    editor.cursor_tick = 0

                    editor.current_symbol += 1
                    if editor.current_symbol > len(editor.lines[editor.current_line]):
                        if editor.current_line < len(editor.lines) - 1:
                            editor.current_symbol = 0
                            editor.current_line += 1
                        else:
                            editor.current_symbol = len(editor.lines[editor.current_line])

                elif event.key == pygame.K_UP:
                    editor.cursor_visible = True
                    editor.cursor_tick = 0

                    editor.current_line -= 1

                    if editor.current_line >= 0:
                        editor.current_symbol = min(editor.current_symbol, len(editor.lines[editor.current_line]))
                    else:
                        editor.current_line = 0

                elif event.key == pygame.K_DOWN:
                    editor.cursor_visible = True
                    editor.cursor_tick = 0

                    editor.current_line += 1

                    if editor.current_line == len(editor.lines):
                        editor.current_line = len(editor.lines) - 1
                    else:
                        editor.current_symbol = min(editor.current_symbol, len(editor.lines[editor.current_line]))

                elif event.key == pygame.K_TAB:
                    editor.add(editor.tab)

                elif event.key == pygame.K_RETURN:
                    editor.new_line()

                else:
                    symbol = event.unicode
                    if symbol:
                        editor.add(symbol)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    backspace_pressed = False
                    backspace_pressed_tick = 0

        if backspace_pressed:
            backspace_pressed_tick += dt

        keys = pygame.key.get_pressed()
        if backspace_pressed_tick >= 30:
            if keys[pygame.K_BACKSPACE]:
                backspace_tick += dt
                if backspace_tick >= 4:
                    backspace_tick = 0
                    editor.delete()

        screen.fill(BLACK)

        editor.update(dt)
        status_bar.update(dt)
        pygame.display.update(pygame.Rect(0, 0, WIDTH, HEIGHT))
        # pygame.display.set_caption(f'{(editor.current_line, editor.current_symbol)}')
        clock.tick()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()

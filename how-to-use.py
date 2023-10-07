import pygame

from pygame_texteditor import TextEditor

# minimal pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pygame")
pygame.display.get_surface().fill((200, 200, 200))  # background coloring

# Instantiation & customization of the text editor
TX = TextEditor(offset_x=50, offset_y=50, editor_width=500, editor_height=400, screen=pygame.display.get_surface())
TX.set_line_numbers(True)
TX.set_syntax_highlighting(True)
TX.set_font_size(18)

# TextEditor in the pygame-loop
while True:
    # INPUT - Mouse + Keyboard
    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # displays editor functionality once per loop
    TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)
    pygame.display.flip()  # updates pygame window

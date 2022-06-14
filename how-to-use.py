import pygame
from pygame_texteditor.TextEditor import TextEditor

# minimal pygame setup
pygame.init()
screenHeight = 500
screenWidth = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Pygame")
pygame.display.get_surface().fill((200, 200, 200))  # background coloring

# parameters
screen = pygame.display.get_surface()  # get existing pygame window/screen
offset_X = 50  # offset from the left border of the pygame window
offset_Y = 50  # offset from the top border of the pygame window
textAreaHeight = 400
textAreaWidth = 500

# instantiation
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen)
TX.set_cursor_mode("blinking")
TX.set_line_numbers(True)
TX.set_syntax_highlighting(True)
TX.set_font_size(20)

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

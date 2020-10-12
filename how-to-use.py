import pygame
from pygametexteditor import TextEditor

# minimal pygame setup
pygame.init()
screenHeight = 600
screenWidth = 900
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Pygame")
pygame.display.get_surface().fill((200, 200, 200))  # background coloring

# parameters
screen = pygame.display.get_surface()  # get existing pygame window/screen
offset_X = 50  # offset from the left border of the pygame window
offset_Y = 50  # offset from the top border of the pygame window
textAreaHeight = 500
textAreaWidth = 800

# instantiation
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen)
TX.set_line_numbers(True)
TX.set_syntax_highlighting(True)
TX.set_colorscheme("dark")

# TextEditor in the pygame-loop
c = 0
while True:
    # INPUT - Mouse + Keyboard
    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y)  # displays editor functionality once per loop
    pygame.display.flip()  # updates pygame window

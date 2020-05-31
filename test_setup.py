import pygame
from pygametexteditor import TextEditor

# Pygame window setup
pygame.init()
systemWidth = 900
systemHeight = 600
screen = pygame.display.set_mode((systemWidth, systemHeight))
pygame.display.set_caption("TextEditor Setup")
pygame.display.get_surface().fill((200, 200, 200))  # background

# TextEditor setup variables
offset_X = 50
offset_Y = 100
codingAreaHeight = 400
codingAreaWidth = 700
displayLineNumbers = True
FPS = 30
clock = pygame.time.Clock()

########################
texteditor = TextEditor(offset_X, offset_Y, codingAreaWidth, codingAreaHeight, screen, displayLineNumbers)

# Editor game-loop
while True:
    texteditor.display_CodeEditor()
    pygame.display.flip()
    clock.tick(FPS)
    print(clock.get_fps())
########################





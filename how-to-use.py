import pygame
from pygametexteditor import TextEditor

pygame.init()
systemHeight = 600
systemWidth = 900
screen = pygame.display.set_mode((systemWidth, systemHeight))
pygame.display.set_caption("TextEditor Setup")
pygame.display.get_surface().fill((200, 200, 200))  # background

# TextEditor setup + parameters
myscreen = pygame.display.get_surface()
offset_X = 50
offset_Y = 50
textAreaHeight = 500
textAreaWidth = 800
displayLineNumbers = True
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, myscreen, displayLineNumbers)

# Editor loop
while True:
    TX.display_CodeEditor()  # has to be called once per loop to capture input
    pygame.display.flip()

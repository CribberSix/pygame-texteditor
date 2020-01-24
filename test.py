import pygame
from TextEditor import TextEditorClass

# pygame setup
pygame.init()
systemWidth = 900
systemHeight = 600
screen = pygame.display.set_mode((systemWidth, systemHeight))  #, pygame.FULLSCREEN)

pygame.display.set_caption("TextEditor Setup")
pygame.display.get_surface().fill((200, 200, 200))  # background

# text editor setup
offset_X = 50
offset_Y = 100
codingAreaHeight = 400
codingAreaWidth = 700
displayLineNumbers = True
TEC = TextEditorClass(offset_X, offset_Y, codingAreaWidth, codingAreaHeight, screen, displayLineNumbers)
# loop
FPS = 30
clock = pygame.time.Clock()
while True:
    TEC.display_CodeEditor()
    pygame.display.flip()
    clock.tick(FPS)
    #print(clock.get_fps())



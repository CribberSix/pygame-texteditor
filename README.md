# A WYSIWYG-texteditor based on pygame



## Usage

The text editor can be inserted into any existing pygame window. Here is a minimal example of it being activated within a 


´´´
screen = 
offset_X = 50
offset_Y = 50
codingAreaHeight = 400
codingAreaWidth = 700
displayLineNumbers = True
FPS = 30
clock = pygame.time.Clock()

TX = TextEditor(offset_X,offset_Y, codingAreaWidth,codingAreaHeight, screen)  # X_offset, Y_offset, codeAreaWidth, codeAreaHeight   # TODO: (check how high I actually want it to be!)

# Editor game-loop
while True:
    TX.display_CodeEditor()
    pygame.display.flip()
    clock.tick(FPS)
    print(clock.get_fps())
########################
´´´

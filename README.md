# A WYSIWYG-texteditor based on pygame

Currently under development. 

## Usage

The text editor can be inserted into any existing pygame window. 
A minimal example of it being activated within an existing pygame window can be found in the file how-to-use.py, or below.

The texteditor takes 5 obligatory parameters and 1 optional parameter.

##### Obligatory
- offset_X : integer (offset from the left border of the pygame screen)
- offset_y : integer (offset from the top border of the pygame screen)
- textAreaWidth : integer (width of texteditor area)
- textAreaHeight : integer (height of texteditor area)
- screen : pygame display surface (on which the texteditor is to be displayed)

##### Optional
- lineNumbers : boolean (if true, display linenumbers)

```

# TextEditor parameters
screen = pygame.display.get_surface()  # get existing pygame window/screen
offset_X = 50  # offset from the left border of the pygame window
offset_Y = 50  # offset from the top border of the pygame window
textAreaHeight = 500
textAreaWidth = 800
lineNumbers = True

# TextEditor setup
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen, lineNumbers)

# TextEditor in the pygame-loop
while True:
    TX.display_CodeEditor()  # has to be called once per loop to capture input
    pygame.display.flip()

```

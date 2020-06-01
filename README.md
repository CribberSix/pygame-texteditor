# A WYSIWYG-texteditor based on pygame

## Project status

The texteditor is currently under development. More features (e.g. copy-paste, shift+strg+arrow highlighting and other common texteditor functions) will be implemented in the future.
Additional parameters and customization options for the editor are planned. 

## Usage

The text editor can be inserted into any existing pygame window. 
A minimal example of it being activated within an existing pygame window can be found below.

The texteditor takes 5 obligatory parameters and 1 optional parameter.

##### Obligatory parameters
- ```offset_X``` : integer (offset from the left border of the pygame screen)
- ```offset_y``` : integer (offset from the top border of the pygame screen)
- ```textAreaWidth``` : integer (width of texteditor area)
- ```textAreaHeight``` : integer (height of texteditor area)
- ```screen``` : pygame display surface (on which the texteditor is to be displayed)

##### Optional parameters
- ```lineNumbers``` : boolean (display line numbers if true, default = true)


###### Minimal pygame setup

```
import pygame
from pygametexteditor import TextEditor

pygame.init()
screenHeight = 600
screenWidth = 900
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Pygame")
pygame.display.get_surface().fill((200, 200, 200))  # background coloring

```
###### Minimal texteditor setup
```
# parameters
screen = pygame.display.get_surface()  # get existing pygame window/screen
offset_X = 50  # offset from the left border of the pygame window
offset_Y = 50  # offset from the top border of the pygame window
textAreaHeight = 500
textAreaWidth = 800
lineNumbers = True

# instantiation
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen, lineNumbers)

# TextEditor in the pygame-loop
while True:
    # the method display_editor() has to be called once per loop to capture input accurately
    TX.display_editor()  

    pygame.display.flip() # updates pygame window

```

##### Retrieving text from the editor

The editor offers the function ```get_text()``` to retrieve the entire text including empty lines as a String from the editor. Lines are separated by the new line character ```\n```.

##### Color-scheme customization

The editor offers various methods to customize the color-scheme. All methods take three parameters for the traditional rgb code (red, green, blue). Below are the methods and the default color values.

- ```set_color_background``` (40, 44, 52)
- ```set_color_Scrollbarbackground``` (40, 44, 52)
- ```set_color_text``` (171, 178, 191)
- ```set_color_lineNumber``` (73, 81, 97)
- ```set_color_lineNumberBackground``` (40, 44, 52) 

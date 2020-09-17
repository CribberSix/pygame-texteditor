# A WYSIWYG-texteditor based on pygame for pygame

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

# instantiation
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen)

# TextEditor in the pygame-loop
while True:
    # the method display_editor() has to be called once per loop to capture input accurately
    TX.display_editor()  

    pygame.display.flip() # updates pygame window

```

##### Retrieving text from the editor

The editor offers the function ```get_text()``` to retrieve the entire text including empty lines as a String from the editor. Lines are separated by the new line character ```\n```.

## Customization

##### Line Numbers 
- Enable line numbers: ```set_line_numbers(True)```

##### Color-scheme customization

The editor uses customizable yaml files to customize the color-scheme. The yaml files are in the folder ```pygametexteditor/elements/colorstyles/```. 
All keys must be present in the file and must have a value. Acceptable values are rgb strings in the following format: ```(255, 255, 255)``` or ```255, 255, 255```.

Editor colors by keys:
- ```codingBackgroundColor```
- ```codingScrollBarBackgroundColor```
- ```lineNumberColor```
- ```lineNumberBackgroundColor```
- ```textColor```

The following keys are used when syntax highlighting is turned on:
- ```textColor_comments```
- ```textColor_quotes```
- ```textColor_operators```
- ```textColor_keywords```

##### Syntax Highlighting

The editor comes with syntax highlighting for Python code. 
Different colors are set for quoted characters (single and double-quotes), comments, numbers and operators. 

Different color-schemes (dark/bright) and more customization options will be implemented in the future. 

- Enbable syntax highlighting: ```set_syntax_coloring(True)``` 


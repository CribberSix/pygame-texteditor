# A WYSIWYG-texteditor based on pygame for pygame

## Project status

The texteditor is currently under development. More features (e.g. copy-paste, shift+strg+arrow highlighting and other common texteditor functions) will be implemented in the future.

## Usage

The text editor can be inserted into any existing pygame window. 
A minimal example of it being activated within an existing pygame window can be found below.

The texteditor takes 5 obligatory parameters and 3 optional parameters.

##### Obligatory parameters
- ```offset_X``` : integer - the offset from the left border of the pygame screen
- ```offset_y``` : integer - the offset from the top border of the pygame screen
- ```textAreaWidth``` : integer - the width of texteditor
- ```textAreaHeight``` : integer - the height of texteditor
- ```screen``` : pygame display surface - on which the texteditor is to be displayed

##### Optional Parameters with default values

- ```line_numbers_flag``` - a boolean enabling showing line numbers 
    > Default: ```False```
- ```style``` - a String setting the color scheme of editor and syntax highlighting 
    > Default: ```'dark'```
- ```syntax_highlighting_flag``` - a boolean enabling syntax highlighting for Python code 
    > Default: ```False```

#### Setup

##### Minimal pygame setup

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
##### Minimal texteditor setup
```
# parameters
screen = pygame.display.get_surface()  # get existing pygame window/screen
offset_X = 50  # offset from the left border of the pygame window
offset_Y = 50  # offset from the top border of the pygame window
textAreaHeight = 500
textAreaWidth = 800


# Instantiation
TX = TextEditor(offset_X, offset_Y, textAreaWidth, textAreaHeight, screen)

# TextEditor in a loop
while True:
    TX.display_editor()  # displays editor functionality - has to be called once per loop to capture input accurately
    pygame.display.flip()  # updates pygame window

```

##### Retrieving text from the editor

The editor offers the function ```get_text()``` to retrieve the entire text including empty lines as a String from the editor. Lines are separated by the new line character ```\n```.

## Customization

##### Line Numbers 
Line numbers can be shown on the left side of the editor. Line numbers begin with 0 as is the Pythonian way. 

Line numbers can be enabled and disabled with ```set_line_numbers(Boolean)```.

##### Color-scheme customization

The editor uses yaml files to customize the color-scheme. The yaml files are stored in the project folder ```pygametexteditor/elements/colorstyles/```. 
All keys must be present with values. Acceptable values are rgb strings in the following format: ```(255, 255, 255)``` or ```255, 255, 255```.

Any arbitrary names can be used for the style. A file named ```stylename.yml``` specifies the RGB colors by keys. 
Per default the editor comes with two different color-schemes (```dark``` and ```bright```).

The following keys are required in the ```stylename.yml``` file:
- ```codingBackgroundColor```
- ```codingScrollBarBackgroundColor```
- ```lineNumberColor```
- ```lineNumberBackgroundColor```
- ```textColor```

##### Syntax Highlighting

The editor comes with syntax highlighting for Python code. Tokenization is based on the ```pygment``` package. 

Syntax highlighting can be enabled/disabled with ```set_syntax_coloring(Boolean)```.

For the syntax highlighting colors, a file named ```stylename-syntax.yml``` is required. 
All keys must be present with values. Acceptable values are rgb strings in the following format: ```(255, 255, 255)``` or ```255, 255, 255```.
The filename of the syntax-colors has to match the filename for the editor-colors. 

The following keys are required in the ```stylename-syntax.yml``` file:
- ```textColor_normal```
- ```textColor_comments```
- ```textColor_quotes```
- ```textColor_operators```
- ```textColor_keywords```
- ````textColor_function````
- ````textColor_builtin````

##### Setting the color-scheme for editor and syntax

The color scheme can be set with  ```set_colorscheme('dark')```. In this example
- the file ```dark.yml``` is being used for editor-colors.
- If syntax highlighting is enabled, the file ```dark-syntax.yml``` is used for syntax-colors. 

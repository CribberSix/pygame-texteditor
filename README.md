# A WYSIWYG-texteditor based on pygame for pygame

![PyPI](https://img.shields.io/pypi/v/pygame-texteditor?color=%233775A9&label=pypi%20package&style=plastic)
![GitHub](https://img.shields.io/github/license/CribberSix/pygame-texteditor?style=plastic)

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

## Setup

##### Minimal pygame setup

```
import pygame
from pygame_texteditor import TextEditor

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
TX.set_line_numbers(True)  # optional 
TX.set_syntax_highlighting(True)  # optional

while True:  # pygame-loop
    # capture input
    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # display editor functionality once per loop
    TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)

    # update pygame window
    pygame.display.flip()  


```

##### Retrieving text from the editor

The editor offers the function `get_text_as_string()` to retrieve the entire text 
as a String from the editor. Lines are separated by the new line character ```\n```.

The editor offers the function `get_text_as_list()` to retrieve the entire text as a list from the editor. 
Each String-item in the list represents one line from the editor.

##### Removing text from the editor

The editor offers the function `clear_text()` to clear the editor of any text.


##### Inserting text into the editor

Inserting text can be done by using one of the two available functions: 
1. With a list of strings in which each string represents one line, or
2. With a string which includes linebreak characters which get parsed. 

```
set_text_from_list(["First line", "Second Line.", "Third Line."]
set_text_from_string("First line.\nSecond line.\nThird Line")
```

## Customization

#### Key repetition speeds

While a key is being held, multiple key events are being triggered. 
The delay of the first repetition as well as the intervall between all sequential key triggers can be 
customized by using the function `set_key_repetition(delay=300, intervall=30)`. 

From the [official documentation](http://www.pygame.org/docs/ref/key.html#pygame.key.set_repeat): 
> The delay parameter is the number of milliseconds before the first repeated pygame.KEYDOWN event will be sent.
> After that, another pygame.KEYDOWN event will be sent every interval milliseconds.

#### Font size

Font size can be customized with the command `set_font_size(size)` - the parameter is an integer 
with the default value `12` to be able to reset it. 

#### Line Numbers 
Line numbers can be shown on the left side of the editor. Line numbers begin with 0 as is the Pythonian way. 

Line numbers can be enabled and disabled with ```set_line_numbers(Boolean)```.


#### Syntax Highlighting

The editor comes with syntax highlighting for Python code. Tokenization is based on the ```pygment``` package. 

Syntax highlighting can be enabled/disabled with ```set_syntax_coloring(boolean_value)```.

The syntax colors being used are also specified in the yml style file.


#### Color-scheme customization

The editor uses a yml file to set the color-scheme for the editor itself and for the syntax coloring. 

Two styles are delivered with the editor, they can be activated respectively by:
- `set_colorscheme("dark")`
- `set_colorscheme("bright")`

A custom style can be loaded with the following method from a created yml file: 
- `set_colorscheme_from_yaml("X:\path\to\custom\filename.yml")`

All keys must be present with values. Acceptable values are 
RGB colors in the following format: ```(255, 255, 255)``` or ```255, 255, 255```.

The following keys are required in the ```stylename.yml``` file, syntax colors are only used if syntax
highlighting is enabled, but are still required to be included.

*Editor colors*
- `codingBackgroundColor`
- `codingScrollBarBackgroundColor`
- `lineNumberColor`
- `lineNumberBackgroundColor`
- `textColor`

*Syntax colors*
- `textColor_normal`
- `textColor_comments`
- `textColor_quotes`
- `textColor_operators`
- `textColor_keywords`
- `textColor_function`
- `textColor_builtin`


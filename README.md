# A WYSIWYG-texteditor based on pygame

Currently under development. 

## Usage

The text editor can be inserted into any existing pygame window. A minimal example of it being activated within an existing pygame window can be found in the file how-to-use.py. 

The texteditor takes 5 obligatory and 1 optional parameter:
- offset_X : integer (offset from the left border of the pygame screen)
- offset_y : integer (offset from the top border of the pygame screen)
- codingAreaWidth : integer (width of texteditor area)
- codingAreaHeight : integer (height of texteditor area)
- screen : pygame display surface (on which the texteditor is to be displayed)
- lineNumbers : boolean (if true, display linenumbers)

```
TX = TextEditor(offset_X, offset_Y, codingAreaWidth, codingAreaHeight, screen, lineNumbers)
```

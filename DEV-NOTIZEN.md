# PyBrainzz

# MOUSE BEHAVIOR - ~~Click~~ vs Drag

**There is no "mouse click"**. There is only:

- MouseDOWN - which sets the following variables:
    - drag_chosen_LineIndex_start
    - drag_chosen_LetterIndex_start
- MouseUP - which sets the following variables:
    - drag_chosen_LineIndex_end
    - drag_chosen_LetterIndex_end

If the two have the same position (line_index + letter_index) then it is a "**click**" as it functions like a click, if the two have a different start- and end-point, then we drag and highlight some text between the two points.

The following variables are used when typing to keep the caret in the correct place. They are also set AFTER a mouse drag has been finished.

- chosen_LetterIndex
- chosen_LineIndex

The variables are set to the END of the mouse drag action (z.b. drag_chosen_LetterIndex_end)

### Caret

The caret is solely set via the variables

- caret_x
- caret_y

### self.dragged_finished

An area **is being** highlighted.

Is set to FALSE upon left mouse DOWN

Is set to TRUE upon left mouse UP

### self.dragged_active

An area **was** highlighted **or is being** highlighted.

Is set to TRUE upon left mouse DOWN

Is set to FALSE upon an input (key or mouse-click) after a area was highlighted → signals that the highlighted area undergoes changes based on the input

- key-input → is being modified/replaced
- the mouse was clicked somewhere else → nothing happens, deselection
- arrow-key → nothing happens, deselection

# Logical vs visual text

The logical text is stored in an list of strings called ```self.line_String_array```.

The visual text is stored in an list of lists of dicts called ```self.line_Text_array```.
For every line, there exists one sublist. The sublists are populated with surfaces which represent
the differently blitted words / operators etc, based on syntax highlighting. If syntax highlighting
is disabled, the sublist contains only one dict with the entire text.

The dicts have three keys:
- ```chars```: actual characters making up the portion of the text
- ```type```: String, describing the content, e.g. 'quoted'
- ```color```: rgb-color code, e.g. (0,0,0)

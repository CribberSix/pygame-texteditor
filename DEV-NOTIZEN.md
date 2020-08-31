# PyBrainzz

# MOUSE BEHAVIOR - ~~Click~~ vs Drag

**There is no "mouse click"**. There is only: 

- MouseDOWN - which sets the following variables:
    - drag_chosen_LineIndex_start
    - drag_chosen_LetterIndex_start
- MouseUP - which sets the following variables:
    - drag_chosen_LineIndex_end
    - drag_chosen_LetterIndex_end

If the two have the same position (line_index + letter_index) then it is a "**click**" as in as it functions like a click, if the two have a different start- and end-point, then we drag and highlight some text between the two points. 

The following variables are used when typing to keep the caret in the correct place. They are also set AFTER a mouse drag has been finished.

- chosen_LetterIndex
- chosen_LineIndex

The variables are set to the END of the mouse drag action (z.b. drag_chosen_LetterIndex_end)

### Cursor

The cursor is solely set via the variables

- cursor_X
- cursor_Y

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
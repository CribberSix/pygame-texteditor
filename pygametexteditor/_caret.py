from ._line_getters import get_line_index, get_letter_index, get_number_of_letters_in_line_by_mouse, \
    get_number_of_letters_in_line_by_index


def set_drag_start_by_mouse(self, mouse_x, mouse_y) -> None:
    # get line
    self.drag_chosen_LineIndex_start = get_line_index(self, mouse_y)

    # end of line
    if get_number_of_letters_in_line_by_mouse(self, mouse_y) < get_letter_index(self, mouse_x):
        self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])

    else:  # within existing line
        self.drag_chosen_LetterIndex_start = int(
            (mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)


def set_drag_end_by_mouse(self, mouse_x, mouse_y) -> None:
    # get line
    self.drag_chosen_LineIndex_end = get_line_index(self, mouse_y)

    # end of line
    if get_number_of_letters_in_line_by_mouse(self, mouse_y) < get_letter_index(self, mouse_x):
        self.drag_chosen_LetterIndex_end = len(self.line_String_array[self.drag_chosen_LineIndex_end])

    else:  # within existing line
        self.drag_chosen_LetterIndex_end = int((mouse_x - self.xline_start) / self.letter_size_X)


def set_drag_start_after_last_line(self) -> None:
    # select last line
    self.drag_chosen_LineIndex_start = self.maxLines - 1
    # select last letter of the line
    self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])


def set_drag_end_after_last_line(self) -> None:
    # select last line
    self.drag_chosen_LineIndex_end = self.maxLines - 1
    # select last letter of the line
    self.drag_chosen_LetterIndex_end = len(self.line_String_array[self.drag_chosen_LineIndex_end])


def update_caret_position_by_drag_start(self) -> None:
    """
    # Updates cursor_X and cursor_Y positions based on the start position of a dragging operation.
    """
    # X Position
    self.cursor_X = self.xline_start + (self.drag_chosen_LetterIndex_start * self.letter_size_X)
    # Y Position
    self.cursor_Y = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap) - \
                    (self.showStartLine * self.lineHeight)


def update_caret_position_by_drag_end(self) -> None:
    """
    # Updates cursor_X and cursor_Y positions based on the end position of a dragging operation.
    """
    # X Position
    self.cursor_X = self.xline_start + (self.drag_chosen_LetterIndex_end * self.letter_size_X)
    # Y Position
    self.cursor_Y = self.editor_offset_Y + (self.drag_chosen_LineIndex_end * self.line_gap) - \
                    (self.showStartLine * self.lineHeight)


def update_caret_position(self) -> None:
    """
    # Updates cursor_X and cursor_Y positions based on current position by line and letter indices
    """
    self.cursor_X = self.xline_start + (self.chosen_LetterIndex * self.letter_size_X)

    self.cursor_Y = self.editor_offset_Y + (self.chosen_LineIndex * self.line_gap) - \
                    (self.showStartLine * self.lineHeight)


def update_caret_position_by_mouse_coordinates(self, mouse_x, mouse_y) -> None:
    """
    # Updates cursor_X and cursor_Y positions based on current position of the mouse
    """
    pass  # TODO: caret positioning during mouse drag

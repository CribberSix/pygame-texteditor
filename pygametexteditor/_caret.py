

def set_drag_start_by_mouse(self, mouse_x, mouse_y) -> None:
    # get line
    self.drag_chosen_LineIndex_start = self.get_line_index(mouse_y)

    # end of line
    if self.get_number_of_letters_in_line_by_mouse(mouse_y) < self.get_letter_index(mouse_x):
        self.drag_chosen_LetterIndex_start = len(self.line_string_list[self.drag_chosen_LineIndex_start])

    else:  # within existing line
        self.drag_chosen_LetterIndex_start = self.get_letter_index(mouse_x)


def set_drag_end_by_mouse(self, mouse_x, mouse_y) -> None:
    """
    Compact method to set both line and letter of drag_end based on mouse coordinates.
    """
    # set line
    self.set_drag_end_line_by_mouse(mouse_y)
    # set letter
    self.set_drag_end_letter_by_mouse(mouse_x)


def set_drag_end_line_by_mouse(self, mouse_y) -> None:
    """
    Sets self.drag_chosen_LineIndex_end by mouse_y.
    """
    self.drag_chosen_LineIndex_end = self.get_line_index(mouse_y)


def set_drag_end_letter_by_mouse(self, mouse_x) -> None:
    """
    Sets self.drag_chosen_LetterIndex_end by mouse_x.
    Dependent on self.drag_chosen_LineIndex_end.
    """
    # end of line
    if self.get_letter_index(mouse_x) > self.get_number_of_letters_in_line_by_index(self.drag_chosen_LineIndex_end):
        self.drag_chosen_LetterIndex_end = len(self.line_string_list[self.drag_chosen_LineIndex_end])
    else:  # within existing line
        self.drag_chosen_LetterIndex_end = self.get_letter_index(mouse_x)


def set_drag_start_after_last_line(self) -> None:
    # select last line
    self.drag_chosen_LineIndex_start = self.maxLines - 1
    # select last letter of the line
    self.drag_chosen_LetterIndex_start = len(self.line_string_list[self.drag_chosen_LineIndex_start])


def set_drag_start_before_first_line(self) -> None:
    self.drag_chosen_LineIndex_start = 0
    self.drag_chosen_LetterIndex_start = 0


def set_drag_end_after_last_line(self) -> None:
    # select last line
    self.drag_chosen_LineIndex_end = self.maxLines - 1
    # select last letter of the line
    self.drag_chosen_LetterIndex_end = len(self.line_string_list[self.drag_chosen_LineIndex_end])


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

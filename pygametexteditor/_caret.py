from ._line_getters import get_line_index, get_letter_index, get_number_of_letters_in_line_by_mouse, \
    get_number_of_letters_in_line_by_index


def set_caret_x_position_by_mouse(self, mouse_x, mouse_y) -> None:
    # end of line
    if get_number_of_letters_in_line_by_mouse(self, mouse_y) < get_letter_index(self, mouse_x):
        self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])
        self.drag_cursor_X_start = self.xline_start + (
                len(self.line_String_array[self.drag_chosen_LineIndex_start]) * self.letter_size_X)
    # within existing line
    else:
        self.drag_chosen_LetterIndex_start = int(
            (mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)
        self.drag_cursor_X_start = self.editor_offset_X + self.xline_start_offset + (
                self.drag_chosen_LetterIndex_start * self.letter_size_X)
    # print("self.drag_chosen_LetterIndex_start: " + str(self.drag_chosen_LetterIndex_start))


def set_caret_y_position_by_mouse(self, mouse_y) -> None:
    self.drag_chosen_LineIndex_start = get_line_index(self, mouse_y)
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap) - (
                self.showStartLine * self.lineHeight)
    # print("self.drag_chosen_LineIndex_start: " + str(self.drag_chosen_LineIndex_start))


def set_caret_start_after_last_line(self) -> None:

    # select last line
    self.drag_chosen_LineIndex_start = self.maxLines - 1
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap) - (
            self.showStartLine * self.lineHeight)

    # select last letter of the line
    self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])
    self.drag_cursor_X_start = self.xline_start + (
            len(self.line_String_array[self.drag_chosen_LineIndex_start]) * self.letter_size_X)


def set_caret_end_after_last_line(self) -> None:
    # select last line - since it's only possible to click after the last line, if there are less lines than
    # possible to be visible, we don't need to subtract anything from the offset+(chosenLineIndex*linegap)
    self.drag_chosen_LineIndex_end = self.maxLines - 1
    self.drag_cursor_Y_end = self.editor_offset_Y + (self.drag_chosen_LineIndex_end * self.line_gap)

    # select last letter of the line
    self.drag_chosen_LetterIndex_end = len(self.line_String_array[self.drag_chosen_LineIndex_end])
    self.drag_cursor_X_end = self.xline_start + (self.drag_chosen_LetterIndex_end * self.letter_size_X)

    self.update_caret_coordinates()


def update_caret_coordinates(self) -> None:
    """
    # Updates cursor_X and cursor_Y positions based on current position by line and letter indices
    """
    self.cursor_X = self.editor_offset_X + self.xline_start_offset + \
                               (self.chosen_LetterIndex * self.letter_size_X)

    self.cursor_Y = self.editor_offset_Y + (self.chosen_LineIndex * self.line_gap) - \
                               (self.showStartLine * self.lineHeight)

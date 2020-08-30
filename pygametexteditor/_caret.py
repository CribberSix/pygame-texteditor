
def set_cursor_x_position(self, mouse_x, mouse_y):
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
    #print("self.drag_chosen_LetterIndex_start: " + str(self.drag_chosen_LetterIndex_start))


def set_cursor_y_position(self, mouse_y):
    self.drag_chosen_LineIndex_start = get_line_index(self, mouse_y)
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap) - (
                self.showStartLine * self.lineHeight)
    #print("self.drag_chosen_LineIndex_start: " + str(self.drag_chosen_LineIndex_start))


def set_cursor_after_last_line(self):
    self.drag_chosen_LineIndex_start = self.maxLines - 1  # go to the end of the last line
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap)
    # Last letter of the line
    self.drag_chosen_LetterIndex_start = get_number_of_letters_in_line_by_index(self, self.drag_chosen_LineIndex_start)
    self.drag_cursor_X_start = self.editor_offset_X + self.xline_start_offset + (
                self.drag_chosen_LetterIndex_start * self.letter_size_X)


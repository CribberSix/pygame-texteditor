def jump_to_start(self, line_start, line_end, letter_start, letter_end) -> None:
    """
    Chosen LineIndex set to start of highlighted area
    """
    if line_start <= line_end:
        # downward highlight or the same line
        self.chosen_line_index = line_start
        self.chosen_letter_index = letter_start
    else:  # upward highlight
        self.chosen_line_index = line_end
        self.chosen_letter_index = letter_end


def jump_to_end(self, line_start, line_end, letter_start, letter_end) -> None:
    """
    Chosen LineIndex set to end of highlighted area
    """
    if line_start <= line_end:
        # downward highlight or the same line
        self.chosen_line_index = line_end
        self.chosen_letter_index = letter_end
    else:  # upward highlight
        self.chosen_line_index = line_start
        self.chosen_letter_index = letter_start


def reset_after_highlight(self) -> None:
    """
    Reset caret, clickdown_cycles and dragged booleans.
    """
    self.dragged_active = False  # deactivate highlight
    self.dragged_finished = True  # highlight is finished
    self.update_caret_position()  # update caret position to chosen_Index (Line+Letter)
    self.last_clickdown_cycle = 0  # reset drag-cycle
    self.last_clickup_cycle = -1
    self.render_line_numbers_flag = True

    if len(self.editor_lines) <= self.showable_line_numbers_in_editor:
        self.first_showable_line_index = 0  # update first showable line

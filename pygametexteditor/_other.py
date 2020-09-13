
def jump_to_start(self, line_start, line_end, letter_start, letter_end):
    """
    Chosen LineIndex set to start of highlighted area
    """
    if line_start <= line_end:
        # downward highlight or the same line
        self.chosen_LineIndex = line_start
        self.chosen_LetterIndex = letter_start
    else:  # upward highlight
        self.chosen_LineIndex = line_end
        self.chosen_LetterIndex = letter_end


def jump_to_end(self, line_start, line_end, letter_start, letter_end):
    """
    Chosen LineIndex set to end of highlighted area
    """
    if line_start <= line_end:
        # downward highlight or the same line
        self.chosen_LineIndex = line_end
        self.chosen_LetterIndex = letter_end
    else:  # upward highlight
        self.chosen_LineIndex = line_start
        self.chosen_LetterIndex = letter_start


def reset_after_highlight(self):
    """
    Reset caret, clickdown_cycles and dragged booleans.
    """
    self.dragged_active = False  # deactivate highlight
    self.dragged_finished = True  # highlight is finished
    self.update_caret_position()  # update caret position to chosen_Index (Line+Letter)
    self.last_clickdown_cycle = 0  # reset drag-cycle
    self.last_clickup_cycle = -1


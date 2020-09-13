
def jump_to_start(self, line_start, line_end, letter_start, letter_end):
    """
    Chosen Lineindex set to start of highlighted area
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
    Chosen Lineindex set to end of highlighted area
    """
    if line_start <= line_end:
        # downward highlight or the same line
        self.chosen_LineIndex = line_end
        self.chosen_LetterIndex = letter_end
    else:  # upward highlight
        self.chosen_LineIndex = line_start
        self.chosen_LetterIndex = letter_start


def get_line_index(self, mouse_y) -> int:
    """
    Returns possible line-position of mouse -> does not take into account
    how many lines there actually are!
    """
    return int(
        ((mouse_y - self.editor_offset_y) / self.line_height_including_gap)
        + self.first_showable_line_index
    )


def get_letter_index(self, mouse_x) -> int:
    """
    Returns possible letter-position of mouse.

    The function is independent of any specific line, so we could possibly return a letter_index which
    is bigger than the letters in the line.
    Returns at least 0 to make sure it is possibly a valid index.
    """
    letter = int((mouse_x - self.xline_start) / self.letter_size_x)
    letter = 0 if letter < 0 else letter
    return letter


def get_number_of_letters_in_line_by_mouse(self, mouse_y) -> int:
    line_index = get_line_index(self, mouse_y)
    return get_number_of_letters_in_line_by_index(self, line_index)


def get_number_of_letters_in_line_by_index(self, index) -> int:
    return len(self.editor_lines[index])


def get_showable_lines(self) -> int:
    """
    Return the number of lines which are shown. Less than maximum if less lines are in the array.
    """
    if self.showable_line_numbers_in_editor + self.first_showable_line_index < len(
        self.editor_lines
    ):
        return self.showable_line_numbers_in_editor + self.first_showable_line_index
    else:
        return len(self.editor_lines)


def line_is_visible(self, line) -> bool:
    """
    Calculate whether the line is being shown in the editor
    """
    return (
        self.first_showable_line_index
        <= line
        < self.first_showable_line_index + self.showable_line_numbers_in_editor
    )

import pygame


def get_line_index(self, mouse_y) -> int:
    """
    Returns possible line-position of mouse -> does not take into account
    how many lines there actually are!
    """
    return int(((mouse_y - self.editor_offset_Y) / self.line_gap) + (self.showStartLine))


def get_letter_index(self, mouse_x) -> int:
    """
    Returns possible letter-position of mouse -> does not take into account
    how many letters there actually are in the line!
    """
    return int((mouse_x - self.xline_start) / self.letter_size_X)


def get_number_of_letters_in_line_by_mouse(self, mouse_y):
    line_index = get_line_index(self, mouse_y)
    return get_number_of_letters_in_line_by_index(self, line_index)


def get_number_of_letters_in_line_by_index(self, index):
    return len(self.line_String_array[index])


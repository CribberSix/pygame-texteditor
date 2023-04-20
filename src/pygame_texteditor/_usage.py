import math
from typing import List

import pygame


def get_text_as_string(self) -> str:
    """
    Returns the entire text of the editor as a single string.
    Linebreak characters are used to differentiate between lines.
    :param self:  Texteditor-Class
    :return: String
    """
    return "\n".join(self.editor_lines)


def get_text_as_list(self) -> List:
    """
    Returns the text in it's logical form as a list of lines.
    :param self:  Texteditor-Class
    :return: List of lines containing the text. Lines cane be empty Strings.
    """
    return self.editor_lines


def clear_text(self) -> None:
    """
    Clears the textarea.
    :param self: Texteditor-Class
    :return: None
    """
    # Create lines
    self.editor_lines = [
        "" for _ in range(int(math.floor(self.editor_height / self.letter_height)))
    ]
    self.first_showable_line_index = 0

    # reset caret
    self.first_iteration_boolean = True  # redraws background
    self.render_line_numbers_flag = True
    self.chosen_line_index = 0
    self.chosen_letter_index = 0
    self.dragged_active = False
    self.dragged_finished = True
    self.scrollbar_is_being_dragged = False
    self.drag_chosen_line_index_start = 0
    self.drag_chosen_letter_index_start = 0
    self.drag_chosen_line_index_end = 0
    self.drag_chosen_letter_index_end = 0
    self.last_clickdown_cycle = 0
    self.last_clickup_cycle = 0
    self.cycleCounter = 0
    self.update_caret_position()
    self.cycleCounter = 0


def set_text_from_list(self, text_list) -> None:
    """
    Sets the text of the editor based on a list of strings. Each item in the list represents one line.
    """
    self.clear_text()
    self.editor_lines = text_list
    self.render_line_numbers_flag = True


def set_text_from_string(self, string) -> None:
    """
    Sets the text of the editor based on a string. Linebreak characters are parsed.
    """
    self.clear_text()
    self.editor_lines = string.split("\n")
    self.render_line_numbers_flag = True

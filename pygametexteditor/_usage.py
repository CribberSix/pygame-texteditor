import pygame
import math
from typing import List


def get_text_as_string(self) -> str:
    """
    Returns the entire text of the editor as a single string.
    Linebreak characters are used to differentiate between lines.
    :param self:  Texteditor-Class
    :return: String
    """
    return "\n".join(self.line_String_array)


def get_text_as_array(self) -> List:
    """
    Returns the text in it's logical form as a list of lines.
    :param self:  Texteditor-Class
    :return: List of lines containing the text. Lines cane be empty Strings.
    """
    return self.line_String_array


def clear_text(self) -> None:
    """
    Clears the textarea.
    :param self: Texteditor-Class
    :return: None
    """
    self.line_String_array = []  # LOGIC: Array of actual Strings
    self.line_Text_array = []  # VISUAL: Array of the rendered surfaces
    self.maxLines = int(math.floor(self.textAreaHeight / self.lineHeight))
    self.showStartLine = 0
    for i in range(self.maxLines):  # from 0 to maxLines:
        self.line_String_array.append("")  # Add a line

    # reset caret
    self.chosen_LineIndex = 0
    self.chosen_LetterIndex = 0
    self.dragged_active = False
    self.dragged_finished = True
    self.last_clickdown_cycle = 0
    self.last_clickup_cycle = 0
    self.cycleCounter = 0
    self.update_caret_position()

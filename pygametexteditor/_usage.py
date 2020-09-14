import pygame
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

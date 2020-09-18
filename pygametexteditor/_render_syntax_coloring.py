from typing import List, Dict, Tuple
import re as re
from pygments.lexers import PythonLexer
from pygametexteditor.PybrainzzFormatter import PybrainzzFormatter


def get_single_color_dicts(self) -> List[List[Dict]]:
    """
    Converts the text in the editor based on the line_String_array into a list of lists of dicts.
    Every line is one sublist.
    Since only one color is being applied, we create a list with one dict per line.
    """
    rendering_list = []
    for line in self.line_String_array:
        # appends a single-item list
        rendering_list.append([{'chars': line, 'type': 'normal', 'color': self.textColor}])

    return rendering_list


def get_syntax_coloring_dicts(self) -> List[List[Dict]]:
    """
    Converts the text in the editor based on the line_String_array into a list of lists of dicts.
    Every line is one sublist which contains different dicts based on it's contents.

    We create a dict for every token of every line and include the characters, a pseudo token-type and the color.
    """
    rendering_list = []
    for line in self.line_String_array:
        line_dict = self.formatter.format(self.lexer.get_tokens(line))
        rendering_list.append(line_dict)
    return rendering_list

import os
import re
import pathlib
import yaml
import pygame
from .PybrainzzFormatter import PybrainzzFormatter
from pygments.lexers import PythonLexer


def set_line_numbers(self, b) -> None:
    """
    Activates/deactivates showing the line numbers in the editor
    """
    self.displayLineNumbers = b
    if self.displayLineNumbers:
        self.lineNumberWidth = 27  # line number background width and also offset for text!
        self.xline_start = self.editor_offset_X + self.xline_start_offset
        self.xline = self.editor_offset_X + self.xline_start_offset
    else:
        self.lineNumberWidth = 0
        self.xline_start = self.editor_offset_X
        self.xline = self.editor_offset_X


def set_syntax_highlighting(self, b) -> None:
    """
    Activates / deactivates syntax highlighting.
    If activated, creates the lexer and formatter and sets the formatter's style.
    """
    self.syntax_coloring = b


def set_colorscheme_from_yaml(self, path_to_yaml) -> None:

    def get_rgb_by_key(dict, key):
        return tuple([int(x) for x in re.findall(r'(\d{1,3})', dict[key])])

    try:
        with open(path_to_yaml) as file:
            color_dict = yaml.load(file, Loader=yaml.FullLoader)

            self.codingBackgroundColor = get_rgb_by_key(color_dict, 'codingBackgroundColor')
            self.codingScrollBarBackgroundColor = get_rgb_by_key(color_dict, 'codingScrollBarBackgroundColor')
            self.lineNumberColor = get_rgb_by_key(color_dict, 'lineNumberColor')
            self.lineNumberBackgroundColor = get_rgb_by_key(color_dict, 'lineNumberBackgroundColor')
            self.textColor = get_rgb_by_key(color_dict, 'textColor')

            self.formatter.textColor_normal = get_rgb_by_key(color_dict, 'textColor_normal')
            self.formatter.textColor_comments = get_rgb_by_key(color_dict, 'textColor_comments')
            self.formatter.textColor_quotes = get_rgb_by_key(color_dict, 'textColor_quotes')
            self.formatter.textColor_operators = get_rgb_by_key(color_dict, 'textColor_operators')
            self.formatter.textColor_keywords = get_rgb_by_key(color_dict, 'textColor_keywords')
            self.formatter.textColor_function = get_rgb_by_key(color_dict, 'textColor_function')
            self.formatter.textColor_builtin = get_rgb_by_key(color_dict, 'textColor_builtin')

    except FileNotFoundError:
        raise FileNotFoundError("Could not find the style file '" + path_to_yaml + "'.")
    except KeyError as e:
        raise KeyError("Could not find all necessary color-keys in the style file '" + path_to_yaml + "'. " +
                       "Missing key: " + str(e))


def set_colorscheme(self, style) -> None:
    """
    Sets the color scheme for the editor and for syntax highlighting if the latter is enabled based on
    one of the editor's default styles.
    """
    if style in ("bright", "dark"):
        default_path = str(pathlib.Path(__file__).parent.absolute()) + "\\elements\colorstyles\\" + style + ".yml"
        self.set_colorscheme_from_yaml(default_path)
    else:
        raise ValueError("No default style with the name '" + style + "' available. " +
                         "\n\tAvailable styles are 'dark' and 'bright'. \n\tFor your " +
                         "own custom styles, use the method 'set_colorscheme_from_yaml(path_to_yaml)' " +
                         "and have a look at the docs.")

import os
import re
import pygame
import yaml
from pygametexteditor.PybrainzzFormatter import PybrainzzFormatter
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
    if b:
        self.lexer = PythonLexer()
        self.formatter = PybrainzzFormatter()
        self.formatter.set_colorscheme(self.colorscheme)


def set_colorscheme(self, style) -> None:
    """
    Sets the color scheme for the editor and for syntax highlighting if the latter is enabled
    """

    self.colorscheme = style

    def get_rgb_by_key(dict, key):
        return tuple([int(x) for x in re.findall(r'(\d{1,3})', dict[key])])

    try:
        with open(os.getcwd() + "\pygametexteditor\elements\colorstyles\\" + style + ".yml") as file:
            color_dict = yaml.load(file, Loader=yaml.FullLoader)

            self.codingBackgroundColor = get_rgb_by_key(color_dict, 'codingBackgroundColor')
            self.codingScrollBarBackgroundColor = get_rgb_by_key(color_dict, 'codingScrollBarBackgroundColor')
            self.lineNumberColor = get_rgb_by_key(color_dict, 'lineNumberColor')
            self.lineNumberBackgroundColor = get_rgb_by_key(color_dict, 'lineNumberBackgroundColor')
            self.textColor = get_rgb_by_key(color_dict, 'textColor')

    except FileNotFoundError:  # Default colors (style = dark)
        raise FileNotFoundError("Could not find the style file '" + style + ".yml'.")
    except IndexError:
        raise IndexError("Could not find all necessary color-keys in the style file '" + style + ".yml'.")

    if self.syntax_coloring:  # setting color for syntax highlighter
        self.formatter.set_colorscheme(style)

import pygame
import yaml
import os
import re


def set_line_numbers(self, b) -> None:
    self.displayLineNumbers = b
    if self.displayLineNumbers:
        self.lineNumberWidth = 27  # line number background width and also offset for text!
        self.xline_start = self.editor_offset_X + self.xline_start_offset
        self.xline = self.editor_offset_X + self.xline_start_offset
    else:
        self.lineNumberWidth = 0
        self.xline_start = self.editor_offset_X
        self.xline = self.editor_offset_X


def set_syntax_coloring(self, b) -> None:
    self.syntax_coloring = b


def set_colorcoding(self, style) -> None:

    print(os.getcwd() + '\pygametexteditor\elements\colorstyles\\' + style + ".yml")
    try:
        with open(os.getcwd() + "\pygametexteditor\elements\colorstyles\\" + style + ".yml") as file:
            colors = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        raise FileNotFoundError("No file named '" + style + ".yml' found in the searched directory \\elements\\colorstyles.")

    pattern = r'(\d{1,3})'
    try:
        self.codingBackgroundColor = tuple([int(x) for x in re.findall(pattern, colors['codingBackgroundColor'])])
        self.codingScrollBarBackgroundColor = tuple([int(x) for x in re.findall(pattern, colors['codingScrollBarBackgroundColor'])])
        self.lineNumberColor = tuple([int(x) for x in re.findall(pattern, colors['lineNumberColor'])])
        self.lineNumberBackgroundColor = tuple([int(x) for x in re.findall(pattern, colors['lineNumberBackgroundColor'])])

        self.textColor = tuple([int(x) for x in re.findall(pattern, colors['textColor'])])
        self.textColor_comments = tuple([int(x) for x in re.findall(pattern, colors['textColor_comments'])])
        self.textColor_quotes = tuple([int(x) for x in re.findall(pattern, colors['textColor_quotes'])])
        self.textColor_operators = tuple([int(x) for x in re.findall(pattern, colors['textColor_operators'])])
        self.textColor_keywords = tuple([int(x) for x in re.findall(pattern, colors['textColor_keywords'])])
        self.textColor_function = tuple([int(x) for x in re.findall(pattern, colors['textColor_function'])])
        self.textColor_builtin = tuple([int(x) for x in re.findall(pattern, colors['textColor_builtin'])])
    except KeyError:
        raise KeyError("Not all color-keys were found in " + style + ".yaml. Please complete the file and restart.")

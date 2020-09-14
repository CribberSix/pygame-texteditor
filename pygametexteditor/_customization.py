import pygame


def set_color_background(self, r, g, b):
    self.codingBackgroundColor = (r, g, b)


def set_color_Scrollbarbackground(self, r, g, b):
    self.codingScrollBarBackgroundColor = (r, g, b)


def set_color_text(self, r, g, b):
    self.textColor = (r, g, b)


def set_color_lineNumber(self, r, g, b):
    self.lineNumberColor = (r, g, b)


def set_color_lineNumberBackground(self, r, g, b):
    self.lineNumberBackgroundColor = (r, g, b)


def set_line_numbers(self, b):
    self.displayLineNumbers = b
    if self.displayLineNumbers:
        self.lineNumberWidth = 27  # line number background width and also offset for text!
        self.xline_start = self.editor_offset_X + self.xline_start_offset
        self.xline = self.editor_offset_X + self.xline_start_offset
    else:
        self.lineNumberWidth = 0
        self.xline_start = self.editor_offset_X
        self.xline = self.editor_offset_X


def set_syntax_coloring(self, b):
    self.syntax_coloring = b

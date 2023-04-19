import math
import os
import pathlib
import re

import pygame
import yaml

current_dir = os.path.dirname(__file__)


def set_key_repetition(self, delay=300, interval=30) -> None:
    """
    The delay parameter is the number of milliseconds before the first repeated pygame.KEYDOWN event will be sent.
    After that, another pygame.KEYDOWN event will be sent every interval milliseconds.
    """
    self.key_initial_delay = delay
    self.key_continued_interval = interval
    pygame.key.set_repeat(self.key_initial_delay, self.key_continued_interval)


def set_font_from_ttf(self, absolute_path_to_ttf: str) -> None:
    """
    Sets the font given a ttf file.

    Disclaimer: As the width of a letter (space) is only calculated once after setting the font_size, any fonts that are not
    monospace will lead to the editor not working correctly anymore, as it cannot be determined anymore, between which
    letters the user clicked.
    """
    self.ttf_path = absolute_path_to_ttf

    # force all the font settings to re-render
    set_font_size(self, self.letter_height)


def set_font_size(self, size=16) -> None:
    """Sets the given size as font size and re-calculates necessary changes."""
    self.editor_font = pygame.font.Font(self.ttf_path, size=size)
    self.letter_height = size
    self.letter_width = self.editor_font.render(" ", 1, (0, 0, 0)).get_width()
    self.line_height_including_margin = self.letter_height + self.line_margin
    self.showable_line_numbers_in_editor = int(
        math.floor(self.editor_height / self.line_height_including_margin)
    )
    # As the font size also influences the size of the line numbers, we need to recalculate some their spacing
    self.line_number_width = self.editor_font.render(" ", 1, (0, 0, 0)).get_width() * 2
    self.line_start_x = self.editor_offset_x + self.line_number_width


def set_line_numbers(self, b) -> None:
    """
    Activates/deactivates showing the line numbers in the editor
    """
    self.display_line_numbers = b
    if self.display_line_numbers:
        self.line_number_width = self.editor_font.render(" ", 1, (0, 0, 0)).get_width()
        self.line_start_x = self.editor_offset_x + self.line_number_width
    else:
        self.line_number_width = 0
        self.line_start_x = self.editor_offset_x


def set_syntax_highlighting(self, b) -> None:
    """
    Activates / deactivates syntax highlighting.
    If activated, creates the lexer and formatter and sets the formatter's style.
    """
    self.syntax_highlighting_python = b


def set_colorscheme_from_yaml(self, path_to_yaml) -> None:
    def get_rgb_by_key(dict, key):
        return tuple([int(x) for x in re.findall(r"(\d{1,3})", dict[key])])

    try:
        with open(path_to_yaml) as file:
            color_dict = yaml.load(file, Loader=yaml.FullLoader)

            self.color_coding_background = get_rgb_by_key(
                color_dict, "codingBackgroundColor"
            )
            self.color_scrollbar_background = get_rgb_by_key(
                color_dict, "codingScrollBarBackgroundColor"
            )
            self.color_line_number_font = get_rgb_by_key(color_dict, "lineNumberColor")
            self.color_line_number_background = get_rgb_by_key(
                color_dict, "lineNumberBackgroundColor"
            )
            self.color_text = get_rgb_by_key(color_dict, "textColor")

            self.color_formatter.textColor_normal = get_rgb_by_key(
                color_dict, "textColor_normal"
            )
            self.color_formatter.textColor_comments = get_rgb_by_key(
                color_dict, "textColor_comments"
            )
            self.color_formatter.textColor_quotes = get_rgb_by_key(
                color_dict, "textColor_quotes"
            )
            self.color_formatter.textColor_operators = get_rgb_by_key(
                color_dict, "textColor_operators"
            )
            self.color_formatter.textColor_keywords = get_rgb_by_key(
                color_dict, "textColor_keywords"
            )
            self.color_formatter.textColor_function = get_rgb_by_key(
                color_dict, "textColor_function"
            )
            self.color_formatter.textColor_builtin = get_rgb_by_key(
                color_dict, "textColor_builtin"
            )

    except FileNotFoundError:
        raise FileNotFoundError("Could not find the style file '" + path_to_yaml + "'.")
    except KeyError as e:
        raise KeyError(
            "Could not find all necessary color-keys in the style file '"
            + path_to_yaml
            + "'. "
            + "Missing key: "
            + str(e)
        )


def set_colorscheme(self, style) -> None:
    """
    Sets the color scheme for the editor and for syntax highlighting if the latter is enabled based on
    one of the editor's default styles.
    """
    if style in ("bright", "dark"):
        default_path = os.path.join(
            str(pathlib.Path(__file__).parent.absolute()),
            "elements",
            "colorstyles",
            style + ".yml",
        )
        self.set_colorscheme_from_yaml(default_path)
    else:
        raise ValueError(
            "No default style with the name '"
            + style
            + "' available. "
            + "\n\tAvailable styles are 'dark' and 'bright'. \n\tFor your "
            + "own custom styles, use the method 'set_colorscheme_from_yaml(path_to_yaml)' "
            + "and have a look at the docs."
        )


def set_cursor_mode(self, mode: str = "blinking"):
    if mode == "blinking":
        self.static_cursor = False
    elif mode == "static":
        self.static_cursor = True
    else:
        raise ValueError(
            f"Value '{mode}' is not a valid cursor mode. Set either to 'blinking' or 'static'."
        )

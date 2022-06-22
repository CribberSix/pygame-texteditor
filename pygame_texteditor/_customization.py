import os
import re
import math
import pathlib
import yaml
import pygame


def set_key_repetition(self, delay=300, intervall=30) -> None:
    """
    The delay parameter is the number of milliseconds before the first repeated pygame.KEYDOWN event will be sent.
    After that, another pygame.KEYDOWN event will be sent every interval milliseconds.
    """
    self.key_initial_delay = delay
    self.key_continued_intervall = intervall
    pygame.key.set_repeat(self.key_initial_delay, self.key_continued_intervall)


def set_font_size(self, size=16) -> None:
    """
    Sets the given size as font size and re-calculates necessary changes.
    """
    self.letter_size_Y = size
    current_dir = os.path.dirname(__file__)
    self.courier_font = pygame.font.Font(
        os.path.join(current_dir, "elements/fonts/Courier.ttf"), self.letter_size_Y
    )
    letter_width = self.courier_font.render(" ", 1, (0, 0, 0)).get_width()
    self.letter_size_X = letter_width
    self.line_gap = 3 + self.letter_size_Y
    self.showable_line_numbers_in_editor = int(
        math.floor(self.textAreaHeight / self.line_gap)
    )


def set_line_numbers(self, b) -> None:
    """
    Activates/deactivates showing the line numbers in the editor
    """
    self.displayLineNumbers = b
    if self.displayLineNumbers:
        self.lineNumberWidth = (
            27  # line number background width and also offset for text!
        )
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
        return tuple([int(x) for x in re.findall(r"(\d{1,3})", dict[key])])

    try:
        with open(path_to_yaml) as file:
            color_dict = yaml.load(file, Loader=yaml.FullLoader)

            self.codingBackgroundColor = get_rgb_by_key(
                color_dict, "codingBackgroundColor"
            )
            self.codingScrollBarBackgroundColor = get_rgb_by_key(
                color_dict, "codingScrollBarBackgroundColor"
            )
            self.lineNumberColor = get_rgb_by_key(color_dict, "lineNumberColor")
            self.lineNumberBackgroundColor = get_rgb_by_key(
                color_dict, "lineNumberBackgroundColor"
            )
            self.textColor = get_rgb_by_key(color_dict, "textColor")

            self.formatter.textColor_normal = get_rgb_by_key(
                color_dict, "textColor_normal"
            )
            self.formatter.textColor_comments = get_rgb_by_key(
                color_dict, "textColor_comments"
            )
            self.formatter.textColor_quotes = get_rgb_by_key(
                color_dict, "textColor_quotes"
            )
            self.formatter.textColor_operators = get_rgb_by_key(
                color_dict, "textColor_operators"
            )
            self.formatter.textColor_keywords = get_rgb_by_key(
                color_dict, "textColor_keywords"
            )
            self.formatter.textColor_function = get_rgb_by_key(
                color_dict, "textColor_function"
            )
            self.formatter.textColor_builtin = get_rgb_by_key(
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

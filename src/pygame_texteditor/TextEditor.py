import math
import os
import re
from typing import Optional

import pygame
import yaml
from pygments.lexers import PythonLexer

from .ColorFormatter import ColorFormatter

current_dir = os.path.dirname(__file__)


class TextEditor:
    # Scroll functionality
    # caret
    from ._caret import (set_drag_end_after_last_line, set_drag_end_by_mouse,
                         set_drag_end_letter_by_mouse,
                         set_drag_end_line_by_mouse,
                         set_drag_start_after_last_line,
                         set_drag_start_before_first_line,
                         set_drag_start_by_mouse, update_caret_position,
                         update_caret_position_by_drag_end,
                         update_caret_position_by_drag_start)
    # files for customization of the editor:
    from ._customization import (set_colorscheme, set_colorscheme_from_yaml,
                                 set_cursor_mode, set_font_from_ttf,
                                 set_font_size, set_line_numbers,
                                 set_syntax_highlighting)
    from ._editor_getters import (get_letter_index, get_line_index,
                                  get_number_of_letters_in_line_by_index,
                                  get_number_of_letters_in_line_by_mouse,
                                  get_showable_lines, line_is_visible)
    # input handling KEYBOARD
    from ._input_handling_keyboard import (handle_keyboard_arrow_down,
                                           handle_keyboard_arrow_left,
                                           handle_keyboard_arrow_right,
                                           handle_keyboard_arrow_up,
                                           handle_keyboard_backspace,
                                           handle_keyboard_delete,
                                           handle_keyboard_input,
                                           handle_keyboard_return,
                                           handle_keyboard_space,
                                           handle_keyboard_tab, insert_unicode)
    from ._input_handling_keyboard_highlight import (
        get_highlighted_characters, handle_highlight_and_copy,
        handle_highlight_and_cut, handle_highlight_and_paste,
        handle_input_with_highlight, highlight_all)
    # input handling MOUSE
    from ._input_handling_mouse import (handle_mouse_input,
                                        mouse_within_existing_lines,
                                        mouse_within_texteditor)
    # letter operations (delete, get)
    from ._letter_operations import (delete_entire_line, delete_letter_to_end,
                                     delete_letter_to_letter,
                                     delete_start_to_letter, get_entire_line,
                                     get_line_from_char_to_char,
                                     get_line_from_char_to_end,
                                     get_line_from_start_to_char)
    from ._other import jump_to_end, jump_to_start, reset_after_highlight
    # rendering (basic, highlighting, syntax coloring)
    from ._rendering import (caret_within_texteditor,
                             get_rect_coord_from_indizes,
                             get_rect_coord_from_mouse,
                             render_background_coloring, render_caret,
                             render_line_contents, render_line_numbers,
                             reset_text_area_to_caret,
                             update_line_number_display)
    from ._rendering_highlighting import (highlight_entire_line,
                                          highlight_from_letter_to_end,
                                          highlight_from_letter_to_letter,
                                          highlight_from_start_to_letter,
                                          highlight_lines, render_highlight)
    from ._rendering_syntax_coloring import (get_single_color_dicts,
                                             get_syntax_coloring_dicts)
    from ._scrollbar_vertical import (display_scrollbar,
                                      render_scrollbar_vertical,
                                      scrollbar_down, scrollbar_up)
    from ._usage import (clear_text, get_text_as_list, get_text_as_string,
                         set_text_from_list, set_text_from_string)

    def __init__(
        self,
        offset_x,
        offset_y,
        text_area_width,
        text_area_height,
        screen,
        # TODO: update doc for parameter name change
        display_line_numbers=False,
        style="dark",
        # TODO: update doc for parameter name change
        syntax_highlighting_python=False,
        # TODO: add doc for new parameter:
        font_size=16,
    ):
        self.screen = screen

        # VISUALS
        self.editor_offset_x = offset_x
        self.editor_offset_y = offset_y
        self.editor_width = text_area_width
        self.editor_height = text_area_height
        self.conclusion_bar_height = 18
        self.ttf_path = os.path.join(current_dir, "elements/fonts/Courier.ttf")
        self.editor_font = pygame.font.Font(self.ttf_path, size=font_size)
        self.letter_height = font_size
        self.letter_width = self.editor_font.render(" ", 1, (0, 0, 0)).get_width()
        self.syntax_highlighting_python = syntax_highlighting_python

        # LINES (line height equals the letter height).
        self.max_line_counter = 0
        # Fill the entire editor with empty lines in the beginning
        self.editor_lines = [
            "" for _ in range(int(math.floor(self.editor_height / self.letter_height)))
        ]
        self.first_showable_line_index = 0  # first line, shown at the top of the editor
        self.line_margin = 3
        self.line_height_including_margin = self.letter_height + self.line_margin
        self.showable_line_numbers_in_editor = int(
            math.floor(self.editor_height / self.line_height_including_margin)
        )

        # SCROLLBAR
        # TODO: replace image with PyGame drawn rect
        self.scrollbar_image = pygame.image.load(
            os.path.join(current_dir, "elements/graphics/Scroll_Bar.png")
        ).convert()
        self.scrollbar_width = 8  # must be an even number
        self.padding_between_edge_and_scrollbar = 2

        self.scrollbar: Optional[pygame.Rect] = None
        self.scrollbar_start_y: Optional[int] = None
        self.scrollbar_is_being_dragged: bool = False

        # LINE NUMBERS
        self.display_line_numbers = display_line_numbers
        self.line_number_width = 0
        if self.display_line_numbers:
            self.line_number_width = (
                self.editor_font.render(" ", 1, (0, 0, 0)).get_width() * 2
            )
        self.line_numbers_y = self.editor_offset_y

        # TEXT COORDINATES
        self.chosen_line_index = 0
        self.chosen_letter_index = 0
        self.line_start_y = (
            self.editor_offset_y + self.line_margin
        )  # add initial margin to offset
        self.line_start_x = self.editor_offset_x
        if self.display_line_numbers:
            self.line_start_x += self.line_number_width

        # CURSOR - coordinates for displaying the caret while typing
        self.caret_display_counter = 0
        self.caret_display_intervals_per_second = 5
        self.static_cursor = False
        self.caret_y = self.editor_offset_y
        self.caret_x = self.line_start_x

        # click down - coordinates used to identify start-point of drag
        self.dragged_active = False
        self.dragged_finished = True
        self.drag_chosen_line_index_start = 0
        self.drag_chosen_letter_index_start = 0
        self.last_clickdown_cycle = 0

        # click up  - coordinates used to identify end-point of drag
        self.drag_chosen_line_index_end = 0
        self.drag_chosen_letter_index_end = 0
        self.last_clickup_cycle = 0

        # Colors
        self.color_coding_background = (40, 41, 41)
        self.color_scrollbar = (60, 61, 61)
        self.color_scrollbar_background = (49, 50, 50)
        self.color_line_number_font = (255, 255, 255)
        self.color_line_number_background = (60, 61, 61)
        self.color_text = (255, 255, 255)
        self.color_caret = (255, 255, 255)

        self.lexer = PythonLexer()
        self.color_formatter = ColorFormatter()
        self.set_colorscheme(style)

        # Key input variables+
        self.key_initial_delay = 300
        self.key_continued_interval = 30
        pygame.key.set_repeat(self.key_initial_delay, self.key_continued_interval)

        # Performance enhancing variables
        self.first_iteration_boolean = True
        self.render_line_numbers_flag = True
        self.click_hold_flag = False
        self.cycleCounter = 0  # Used to be able to tell whether a mouse-drag action has been handled already or not.

        self.clock = pygame.time.Clock()
        self.FPS = 60  # we need to limit the FPS so we don't trigger the same actions too often (e.g. deletions)
        self.max_line_number_rendered = len(
            self.editor_lines
        )  # TODO: move to a fitting location.

    def display_editor(
        self, pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed
    ):
        """
        :param pygame_events:
        :param pressed_keys:
        :param mouse_x:
        :param mouse_y:
        :param mouse_pressed:
        """
        # needs to be called within a while loop to be able to catch key/mouse input and update visuals throughout use.
        self.cycleCounter = self.cycleCounter + 1
        # first iteration
        if self.first_iteration_boolean:
            # paint entire area to avoid pixel error beneath line numbers
            pygame.draw.rect(
                self.screen,
                self.color_coding_background,
                (
                    self.editor_offset_x,
                    self.editor_offset_y,
                    self.editor_width,
                    self.editor_height,
                ),
            )
            self.first_iteration_boolean = False

        for event in pygame_events:  # handle QUIT operation
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.handle_keyboard_input(pygame_events, pressed_keys)
        self.handle_mouse_input(pygame_events, mouse_x, mouse_y, mouse_pressed)

        self.update_line_number_display()

        # RENDERING 1 - Background objects
        self.render_background_coloring()
        self.render_line_numbers()

        # RENDERING 2 - Line contents, caret
        self.render_highlight(mouse_x, mouse_y)
        if self.syntax_highlighting_python:
            # syntax highlighting for code
            line_contents = self.get_syntax_coloring_dicts()
        else:
            # single-color text
            line_contents = self.get_single_color_dicts()
        self.render_line_contents(line_contents)
        self.render_caret()

        # RENDERING 3 - scrollbar
        self.render_scrollbar_vertical()
        self.clock.tick(self.FPS)

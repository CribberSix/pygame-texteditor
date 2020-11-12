from pygments.lexers import PythonLexer
from .PybrainzzFormatter import PybrainzzFormatter
import pygame
import math
import os
import yaml
import re


class TextEditor:
    # Scroll functionality
    from ._scrollbar_vertical import render_scrollbar_vertical, display_scrollbar, scrollbar_up, \
        scrollbar_down

    # input handling KEYBOARD
    from ._input_handling_keyboard import handle_keyboard_input, handle_keyboard_delete, handle_keyboard_backspace, \
        handle_keyboard_return, handle_keyboard_space, handle_keyboard_tab, insert_unicode, \
        handle_keyboard_arrow_left, handle_keyboard_arrow_right, handle_keyboard_arrow_up, handle_keyboard_arrow_down

    from ._input_handling_keyboard_highlight import handle_input_with_highlight, handle_highlight_and_copy, \
        handle_highlight_and_paste, handle_highlight_and_cut, highlight_all, get_highlighted_characters

    # input handling MOUSE
    from ._input_handling_mouse import handle_mouse_input, mouse_within_texteditor, mouse_within_existing_lines

    # caret
    from ._caret import update_caret_position, update_caret_position_by_drag_end, update_caret_position_by_drag_start, \
        set_drag_start_after_last_line, set_drag_end_after_last_line, set_drag_start_by_mouse, \
        set_drag_end_by_mouse, set_drag_end_line_by_mouse, set_drag_end_letter_by_mouse, \
        set_drag_start_before_first_line

    # letter operations (delete, get)
    from ._letter_operations import \
        delete_entire_line, delete_start_to_letter, delete_letter_to_end, delete_letter_to_letter, \
        get_entire_line, get_line_from_start_to_char, get_line_from_char_to_end, get_line_from_char_to_char

    # rendering (basic, highlighting, syntax coloring)
    from ._rendering import render_line_contents_by_dicts, \
        render_caret, caret_within_texteditor, render_background_coloring, render_line_numbers, \
        reset_text_area_to_caret, get_rect_coord_from_indizes, get_rect_coord_from_mouse
    from ._rendering_highlighting import render_highlight, highlight_lines, highlight_entire_line, \
        highlight_from_letter_to_letter, highlight_from_start_to_letter, highlight_from_letter_to_end
    from ._rendering_syntax_coloring import get_syntax_coloring_dicts, get_single_color_dicts

    from ._editor_getters import get_line_index, get_letter_index, line_is_visible, get_showable_lines, \
        get_number_of_letters_in_line_by_mouse, get_number_of_letters_in_line_by_index

    from ._other import jump_to_start, jump_to_end, reset_after_highlight

    # files for customization of the editor:
    from ._customization import set_line_numbers, set_syntax_highlighting, set_colorscheme, set_colorscheme_from_yaml
    from ._usage import get_text_as_list, get_text_as_string, clear_text

    def __init__(self, offset_x, offset_y, text_area_width, text_area_height, screen,
                 line_numbers_flag=False, style='dark', syntax_highlighting_flag=False):
        self.screen = screen

        # VISUALS
        self.editor_offset_X = offset_x
        self.editor_offset_Y = offset_y
        self.textAreaWidth = text_area_width
        self.textAreaHeight = text_area_height
        self.conclusionBarHeight = 18
        self.letter_size_Y = 15
        self.letter_size_X = 9
        current_dir = os.path.dirname(__file__)
        self.courier_font = pygame.font.Font(os.path.join(current_dir, "elements/fonts/Courier.ttf"),
                                             self.letter_size_Y)
        self.trennzeichen_image = pygame.image.load(
            os.path.join(current_dir, "elements/graphics/Trennzeichen.png")).convert_alpha()
        self.syntax_coloring = syntax_highlighting_flag

        # LINES
        self.Trenn_counter = 0
        self.MaxLinecounter = 0
        self.line_string_list = []  # LOGIC: Array of actual Strings
        self.lineHeight = 18
        self.showable_line_numbers_in_editor = int(math.floor(self.textAreaHeight / self.lineHeight))

        # self.maxLines is the variable keeping count how many lines we currently have -
        # in the beginning we fill the entire editor with empty lines.
        self.maxLines = int(math.floor(self.textAreaHeight / self.lineHeight))
        self.showStartLine = 0  # first line (shown at the top of the editor) <- must be zero during init!
        self.line_gap = 3 + self.letter_size_Y

        for i in range(self.maxLines):  # from 0 to maxLines:
            self.line_string_list.append("")  # Add a line

        # SCROLLBAR
        self.scrollBarImg = pygame.image.load(os.path.join(current_dir, "elements/graphics/Scroll_Bar.png")).convert()
        self.scrollBarWidth = 8  # must be an even number

        self.scrollbar: pygame.Rect = None
        self.scroll_start_y: int = None
        self.scroll_dragging: bool = False


        # LINE NUMBERS
        self.displayLineNumbers = line_numbers_flag
        if self.displayLineNumbers:
            self.lineNumberWidth = 27  # line number background width and also offset for text!
        else:
            self.lineNumberWidth = 0
        self.line_numbers_Y = self.editor_offset_Y

        # TEXT COORDINATES
        self.chosen_LineIndex = 0
        self.chosen_LetterIndex = 0
        self.yline_start = self.editor_offset_Y + 3
        self.yline = self.editor_offset_Y
        self.xline_start_offset = 28
        if self.displayLineNumbers:
            self.xline_start = self.editor_offset_X + self.xline_start_offset
            self.xline = self.editor_offset_X + self.xline_start_offset
        else:
            self.xline_start = self.editor_offset_X
            self.xline = self.editor_offset_X

        # CURSOR - coordinates for displaying the caret while typing
        self.cursor_Y = self.yline_start - 3
        self.cursor_X = self.xline_start

        # click down - coordinates used to identify start-point of drag
        self.dragged_active = False
        self.dragged_finished = True
        self.drag_chosen_LineIndex_start = 0
        self.drag_chosen_LetterIndex_start = 0
        self.last_clickdown_cycle = 0

        # click up  - coordinates used to identify end-point of drag
        self.drag_chosen_LineIndex_end = 0
        self.drag_chosen_LetterIndex_end = 0
        self.last_clickup_cycle = 0

        # Colors
        self.codingBackgroundColor = (40, 41, 41)
        self.codingScrollBarBackgroundColor = (49, 50, 50)
        self.lineNumberColor = (255, 255, 255)
        self.lineNumberBackgroundColor = (60, 61, 61)
        self.textColor = (255, 255, 255)
        self.color_scrollbar = (60, 61, 61)

        self.lexer = PythonLexer()
        self.formatter = PybrainzzFormatter()
        self.set_colorscheme(style)

        # Performance enhancing variables
        self.deleteCounter = 0
        self.firstiteration_boolean = True
        self.rerenderLineNumbers = True
        self.click_hold = False

        self.cycleCounter = 0  # Used to be able to tell whether a mouse-drag action has been handled already or not.

        self.clock = pygame.time.Clock()
        self.FPS = 60  # we need to limit the FPS so we don't trigger the same actions too often (e.g. deletions)

    def display_editor(self, pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed):
        # needs to be called within a while loop to be able to catch key/mouse input and update visuals throughout use.
        self.cycleCounter = self.cycleCounter + 1
        # first iteration
        if self.firstiteration_boolean:
            # paint entire area to avoid pixel error beneath line numbers
            pygame.draw.rect(self.screen, self.codingBackgroundColor,
                             (self.editor_offset_X, self.editor_offset_Y, self.textAreaWidth, self.textAreaHeight))

            self.firstiteration_boolean = False

        for event in pygame_events:  # handle QUIT operation
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.handle_keyboard_input(pygame_events, pressed_keys)
        self.handle_mouse_input(pygame_events, mouse_x, mouse_y, mouse_pressed)

        # RENDERING 1 - Background objects
        self.render_background_coloring()
        self.render_line_numbers()

        # RENDERING 2 - Lines
        self.render_highlight(mouse_x, mouse_y)

        if self.syntax_coloring:  # syntax highlighting for code
            list_of_dicts = self.get_syntax_coloring_dicts()
        else:  # single-color text
            list_of_dicts = self.get_single_color_dicts()
        self.render_line_contents_by_dicts(list_of_dicts)

        self.render_caret()

        self.render_scrollbar_vertical()
        self.clock.tick(self.FPS)

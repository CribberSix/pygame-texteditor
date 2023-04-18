from typing import Tuple

import pygame


def get_rect_coord_from_mouse(self, mouse_x, mouse_y) -> Tuple[int, int]:
    """Return x and y pixel-coordinates for the position of the mouse."""
    line = self.get_line_index(mouse_y)
    letter = self.get_letter_index(mouse_x)
    return self.get_rect_coord_from_indizes(line, letter)


def get_rect_coord_from_indizes(self, line, letter) -> Tuple[int, int]:
    """Return x and y pixel-coordinates for line and letter by index."""
    line_coord = self.editor_offset_y + (
        self.line_height_including_gap * (line - self.first_showable_line_index)
    )
    letter_coord = self.xline_start + (letter * self.letter_size_x)
    return letter_coord, line_coord


def render_background_coloring(self) -> None:
    """Render background color of the text area."""
    bg_left = self.editor_offset_X + self.line_number_width
    bg_top = self.editor_offset_y
    bg_width = self.editor_width - self.line_number_width
    bg_height = self.editor_height
    pygame.draw.rect(
        self.screen, self.codingBackgroundColor, (bg_left, bg_top, bg_width, bg_height)
    )


def render_line_numbers(self) -> None:
    """Render the line numbers next to the text area.

    While background rendering is done for all "line-slots" (to overpaint remaining "old" numbers without lines)
    we render line-numbers only for existing string-lines.
    """
    if self.display_line_numbers and self.rerender_line_numbers:
        # Render background for the line numbers.
        rect_measurements_background = (
            self.editor_offset_X,
            self.editor_offset_y,
            self.line_number_width,
            self.editor_height,
        )
        pygame.draw.rect(
            self.screen, self.lineNumberBackgroundColor, rect_measurements_background
        )

        # Render the actual line numbers
        line_numbers_y = self.editor_offset_y  # init for first line
        for x in range(
            self.first_showable_line_index,
            self.first_showable_line_index + self.showable_line_numbers_in_editor,
        ):
            if x < self.get_showable_lines():
                rect_measurements = (
                    self.editor_offset_X,
                    line_numbers_y,
                    self.line_number_width,
                    self.line_height_including_gap,
                )
                # x + 1 in order to start with line number "1" instead of index "0".
                text = self.editor_font.render(
                    str(x + 1).zfill(2), 1, self.lineNumberColor
                )
                text_rect = text.get_rect()
                text_rect.center = pygame.Rect(rect_measurements).center
                self.screen.blit(text, text_rect)  # render on center of bg block
            line_numbers_y += self.line_height_including_gap
        self.rerender_line_numbers = False


def render_line_contents_by_dicts(self, dicts) -> None:
    # Preparation of the rendering:
    self.yline = self.yline_start
    first_line = self.first_showable_line_index
    if self.showable_line_numbers_in_editor < len(self.editor_lines):
        # we got more text than we are able to display
        last_line = (
            self.first_showable_line_index + self.showable_line_numbers_in_editor
        )
    else:
        last_line = len(self.editor_lines)

    # Actual line rendering based on dict-keys
    for line_list in dicts[first_line:last_line]:
        xcoord = self.xline_start
        for dict in line_list:
            surface = self.editor_font.render(
                dict["chars"], 1, dict["color"]
            )  # create surface
            self.screen.blit(surface, (xcoord, self.yline))  # blit surface onto screen
            xcoord = xcoord + (
                len(dict["chars"]) * self.letter_size_x
            )  # next line-part prep

        self.yline += self.line_height_including_gap  # next line prep


def caret_within_texteditor(self) -> bool:
    """Check whether the caret's coordinates are within the visible text area.

    If the caret can possibly be in a line which is not currently displayed after using the mouse wheel for scrolling.
    Test for 'self.editor_offset_Y <= self.cursor_Y' as the caret can have the exact same Y-coordinate as the offset if
    the caret is in the first line.

    :return bool:
    """
    return (
        # left border
        self.editor_offset_X + self.line_number_width < self.caret_x <
        # right border
        (
            self.editor_offset_X
            + self.editor_width
            - self.scrollbar_width
            - self.padding_between_edge_and_scrollbar
        )
        and
        # top border
        self.editor_offset_y <= self.caret_y <
        # bottom border
        (self.editor_height + self.editor_offset_y - self.conclusion_bar_height)
    )


def render_caret(self) -> None:
    """
    Called every frame. Displays a cursor for x frames, then none for x frames. Only displayed if line in which
    caret resides is visible and there is no active dragging operation going on.
    Dependent on FPS -> 5 intervalls per second
    Creates 'blinking' animation
    """
    self.trenn_counter += 1
    if self.static_cursor or (
        self.trenn_counter > (self.FPS / 5)
        and self.caret_within_texteditor()
        and self.dragged_finished
    ):
        self.trenn_counter = self.trenn_counter % ((self.FPS / 5) * 2)
        pygame.draw.line(
            surface=self.screen,
            color=self.color_caret,
            start_pos=(self.caret_x, self.caret_y),
            end_pos=(self.caret_x, self.caret_y + self.letter_size_y),
            width=1,
        )


def reset_text_area_to_caret(self) -> None:
    """
    Reset visual area to include the line of caret if it is currently not visible. This function ensures
    that whenever we type, the line in which the caret resides becomes visible, even after scrolling.
    """
    if self.chosen_LineIndex < self.first_showable_line_index:
        # Caret is above the visible area, "jump" to show the line of the caret
        self.first_showable_line_index = self.chosen_LineIndex
        self.rerender_line_numbers = True
        self.update_caret_position()
    elif self.chosen_LineIndex > (
        self.first_showable_line_index + self.showable_line_numbers_in_editor - 1
    ):
        # caret is below visible area, "jump" to show the line of the caret
        self.first_showable_line_index = (
            self.chosen_LineIndex - self.showable_line_numbers_in_editor + 1
        )
        self.rerender_line_numbers = True
        self.update_caret_position()
    # TODO: set caret coordinates

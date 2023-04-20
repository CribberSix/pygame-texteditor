from typing import Dict, Tuple

import pygame


def get_rect_coord_from_mouse(self, mouse_x, mouse_y) -> Tuple[int, int]:
    """Return x and y pixel-coordinates for the position of the mouse."""
    line = self.get_line_index(mouse_y)
    letter = self.get_letter_index(mouse_x)
    return self.get_rect_coord_from_indizes(line, letter)


def get_rect_coord_from_indizes(self, line, letter) -> Tuple[int, int]:
    """Return x and y pixel-coordinates for line and letter by index."""
    line_coord = self.editor_offset_y + (
        self.line_height_including_margin * (line - self.first_showable_line_index)
    )
    letter_coord = self.line_start_x + (letter * self.letter_width)
    return letter_coord, line_coord


def render_background_coloring(self) -> None:
    """Render background color of the text area."""
    bg_left = self.editor_offset_x + self.line_number_width
    bg_top = self.editor_offset_y
    bg_width = self.editor_width - self.line_number_width
    bg_height = self.editor_height
    pygame.draw.rect(
        self.screen,
        self.color_coding_background,
        (bg_left, bg_top, bg_width, bg_height),
    )


def render_line_numbers(self) -> None:
    """Render the line numbers next to the text area.

    While background rendering is done for all "line-slots" (to overpaint remaining "old" numbers without lines)
    we render line-numbers only for existing string-lines.
    """
    if self.display_line_numbers and self.render_line_numbers_flag:
        # Render background for the line numbers.
        rect_measurements_background = (
            self.editor_offset_x,
            self.editor_offset_y,
            self.line_number_width,
            self.editor_height,
        )
        pygame.draw.rect(
            self.screen, self.color_line_number_background, rect_measurements_background
        )

        # Render the actual line numbers
        line_numbers_y = self.editor_offset_y  # init for first line
        for x in range(
            self.first_showable_line_index,
            self.first_showable_line_index + self.showable_line_numbers_in_editor,
        ):
            if x < self.get_showable_lines():
                rect_measurements = (
                    self.editor_offset_x,
                    line_numbers_y,
                    self.line_number_width,
                    self.line_height_including_margin,
                )
                # x + 1 in order to start with line number "1" instead of index "0".
                text = self.editor_font.render(
                    # Prepend line number with spaces to achieve a uniform display:
                    # - the min is 2 characters
                    # - the max is the length of the max line number represented as a string.
                    str(x + 1).rjust(max(2, len(str(len(self.editor_lines))))),
                    1,
                    self.color_line_number_font,
                )
                text_rect = text.get_rect()
                text_rect.center = pygame.Rect(rect_measurements).center
                self.screen.blit(text, text_rect)  # render on center of bg block
            line_numbers_y += self.line_height_including_margin
        self.render_line_numbers_flag = False


def render_line_contents(self, line_contents: Dict) -> None:
    # Preparation of the rendering:
    y_coordinate = self.line_start_y
    first_line = self.first_showable_line_index
    if self.showable_line_numbers_in_editor < len(self.editor_lines):
        # we got more text than we are able to display
        last_line = (
            self.first_showable_line_index + self.showable_line_numbers_in_editor
        )
    else:
        last_line = len(self.editor_lines)

    # Actual line rendering based on dict-keys
    for line_list in line_contents[first_line:last_line]:
        xcoord = self.line_start_x
        for dict in line_list:
            surface = self.editor_font.render(
                dict["chars"], 1, dict["color"]
            )  # create surface
            self.screen.blit(
                surface, (xcoord, y_coordinate)
            )  # blit surface onto screen
            xcoord = xcoord + (
                len(dict["chars"]) * self.letter_width
            )  # next line-part prep

        y_coordinate += self.line_height_including_margin  # next line prep


def caret_within_texteditor(self) -> bool:
    """Check whether the caret's coordinates are within the visible text area.

    If the caret can possibly be in a line which is not currently displayed after using the mouse wheel for scrolling.
    Test for 'self.editor_offset_Y <= self.cursor_Y' as the caret can have the exact same Y-coordinate as the offset if
    the caret is in the first line.

    :return bool:
    """
    return (
        # left border
        self.editor_offset_x + self.line_number_width < self.caret_x <
        # right border
        (
            self.editor_offset_x
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
    Dependent on FPS -> 5 intervals per second
    Creates 'blinking' animation
    """
    self.caret_display_counter += 1
    if self.static_cursor or (
        self.caret_display_counter
        > (self.FPS / self.caret_display_intervals_per_second)
        and self.caret_within_texteditor()
        and self.dragged_finished
    ):
        self.caret_display_counter = self.caret_display_counter % (
            (self.FPS / self.caret_display_intervals_per_second) * 2
        )
        pygame.draw.line(
            surface=self.screen,
            color=self.color_caret,
            start_pos=(self.caret_x, self.caret_y),
            end_pos=(self.caret_x, self.caret_y + self.letter_height),
            width=1,
        )


def reset_text_area_to_caret(self) -> None:
    """
    Reset visual area to include the line of caret if it is currently not visible. This function ensures
    that whenever we type, the line in which the caret resides becomes visible, even after scrolling.
    """
    if self.chosen_line_index < self.first_showable_line_index:
        # Caret is above the visible area, "jump" to show the line of the caret
        self.first_showable_line_index = self.chosen_line_index
        self.render_line_numbers_flag = True
        self.update_caret_position()
    elif self.chosen_line_index > (
        self.first_showable_line_index + self.showable_line_numbers_in_editor - 1
    ):
        # caret is below visible area, "jump" to show the line of the caret
        self.first_showable_line_index = (
            self.chosen_line_index - self.showable_line_numbers_in_editor + 1
        )
        self.render_line_numbers_flag = True
        self.update_caret_position()


def update_line_number_display(self) -> None:
    """Update the display of the line numbers, specifically background width if the number of lines changed.

    If the existing space is not wide enough anymore, e.g. if we go from 99 to 100 lines or from 999 to 1000.
    :return None:
    """
    if len(self.editor_lines) != self.max_line_number_rendered:
        self.line_number_width = self.editor_font.render(
            " ", 1, (0, 0, 0)
        ).get_width() * max(2, len(str(len(self.editor_lines))))
        self.line_start_x = self.editor_offset_x + self.line_number_width
        self.max_line_number_rendered = len(self.editor_lines)

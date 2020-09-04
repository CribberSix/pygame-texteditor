import pygame


def get_showable_lines(self) -> int:
    """
    Return the number of lines which are shown. Less than maximum if less lines are in the array.
    """
    if self.showable_line_numbers_in_editor + self.showStartLine < self.maxLines:
        return self.showable_line_numbers_in_editor + self.showStartLine
    else:
        return self.maxLines


def get_rect_coord_from_mouse(self, mouse_x, mouse_y):
    """
    Return x and y pixel-coordinates for the position of the mouse.
    """
    line = self.get_line_index(mouse_y)
    letter = self.get_letter_index(mouse_x)
    return self.get_rect_coord_from_indizes(line, letter)


def get_rect_coord_from_indizes(self, line, letter) -> (int, int):
    """
    Return x and y pixel-coordinates for line and letter by index.
    """
    line_coord = self.editor_offset_Y + (self.line_gap * (line - self.showStartLine))
    letter_coord = self.xline_start + (letter * self.letter_size_X)
    return letter_coord, line_coord


def render_background_objects(self) -> None:
    """
    Renders background color of the text area.
    Renders line numbers if self.displayLineNumbers = True
    """
    render_background_coloring(self)
    render_line_numbers(self)


def render_background_coloring(self) -> None:
    """
    Renders background color of the text area.
    """
    bg_left = self.editor_offset_X + self.lineNumberWidth
    bg_top = self.editor_offset_Y
    bg_width = self.textAreaWidth - self.scrollBarWidth - self.lineNumberWidth
    bg_height = self.textAreaHeight
    pygame.draw.rect(self.screen, self.codingBackgroundColor, (bg_left, bg_top, bg_width, bg_height))


def render_line_numbers(self) -> None:
    """
    While background rendering is done for all "line-slots" (to overpaint remaining "old" numbers without lines)
    we render line-numbers only for existing string-lines.
    """
    if self.displayLineNumbers and self.rerenderLineNumbers:
        self.rerenderLineNumbers = False
        line_numbers_Y = self.editor_offset_Y  # init for first line
        for x in range(self.showStartLine, self.showStartLine + self.showable_line_numbers_in_editor):

            # background
            pygame.draw.rect(self.screen, self.lineNumberBackgroundColor,
                             (self.editor_offset_X, line_numbers_Y, self.lineNumberWidth, 17))
            # line number
            if x < get_showable_lines(self):
                text = self.courier_font.render(str(x).zfill(2), 1, self.lineNumberColor)
                self.screen.blit(text, (self.editor_offset_X + 5, line_numbers_Y + 3))  # center of bg block

            line_numbers_Y += self.line_gap


def render_line_contents(self) -> None:
    """
    Called every frame. Renders all visible lines.
    Renders highlighted area and actual letters
    """
    self.line_Text_array[self.chosen_LineIndex] = self.courier_font.render(
        self.line_String_array[self.chosen_LineIndex], 1, self.textColor)
    self.yline = self.yline_start

    first_line = self.showStartLine
    if self.showable_line_numbers_in_editor < len(self.line_Text_array):
        # we got more text than we are able to display
        last_line = self.showStartLine + self.showable_line_numbers_in_editor
    else:
        last_line = self.maxLines

    # render all visible lines once per Frame based on the visual array of surfaces
    for line in self.line_Text_array[first_line: last_line]:
        self.screen.blit(line, (self.xline, self.yline))
        self.yline += self.line_gap


def render_highlight(self, mouse_x, mouse_y) -> None:
    """
    Renders highlighted area:
    1. During drag-action -> area starts at drag_start and follows mouse
    2. After drag-action -> area stays confined to selected area by drag_start and drag_end
    """

    if self.dragged_active:  # some text is highlighted or being highlighted
        line_start = self.drag_chosen_LineIndex_start
        letter_start = self.drag_chosen_LetterIndex_start

        if self.dragged_finished:  # highlighting operation is done, user "clicked-up" with the left mouse button
            line_end = self.drag_chosen_LineIndex_end
            letter_end = self.drag_chosen_LetterIndex_end
            self.highlight_lines(line_start, letter_start, line_end, letter_end)  # Actual highlighting

        else:  # active highlighting -> highlighted area follows mouse movements
            line_end = self.get_line_index(mouse_y)
            letter_end = self.get_letter_index(mouse_x)

            # stop highlight not directly at the mouse, but at first or last letter depending on cursor positioning
            if letter_end < 0:
                letter_end = 0
            elif letter_end > len(self.line_String_array[line_end]):
                letter_end = len(self.line_String_array[line_end])

            self.highlight_lines(line_start, letter_start, line_end, letter_end)  # Actual highlighting


def caret_within_texteditor(self) -> bool:
    """
    Tests whether the caret's coordinates are within the visible text area.
    If the caret can possibly be in a line which is not currently displayed after using the mouse wheel for scrolling.
    Test for 'self.editor_offset_Y <= self.cursor_Y' as the caret can have the exact same Y-coordinate as the offset if
    the caret is in the first line.
    """
    return self.editor_offset_X + self.lineNumberWidth < self.cursor_X < (
                self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth) \
           and self.editor_offset_Y <= self.cursor_Y < (
                       self.textAreaHeight + self.editor_offset_Y - self.conclusionBarHeight)


def render_caret(self) -> None:
    """
    Called every frame. Displays a cursor for x frames, then none for x frames. Only displayed if line in which
    caret resides is visible and there is no active dragging operation going on.
    Dependent on FPS -> 5 intervalls per second
    Creates 'blinking' animation
    """
    self.Trenn_counter += 1
    if self.Trenn_counter > (self.FPS / 5) and self.caret_within_texteditor() and self.dragged_finished:
        self.screen.blit(self.trennzeichen_image, (self.cursor_X, self.cursor_Y))
        self.Trenn_counter = self.Trenn_counter % ((self.FPS / 5) * 2)


def reset_text_area_to_caret(self) -> None:
    """
    Reset visual area to include the line of caret if it is currently not visible. This function ensures
    that whenever we type, the line in which the caret resides becomes visible, even after scrolling.
    """
    if self.chosen_LineIndex < self.showStartLine:  # above visible area
        self.showStartLine = self.chosen_LineIndex
        self.rerenderLineNumbers = True
        self.update_caret_position()
    elif self.chosen_LineIndex > (self.showStartLine + self.showable_line_numbers_in_editor - 1):  # below visible area
        self.showStartLine = self.chosen_LineIndex - self.showable_line_numbers_in_editor + 1
        self.rerenderLineNumbers = True
        self.update_caret_position()
    # TODO: set cursor coordinates

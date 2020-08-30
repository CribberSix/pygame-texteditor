import pygame


def get_line_number_string(num) -> str:
    if num < 10:  # 1-digit numbers
        return " " + str(num)
    else:  # 2-digit numbers
        return str(num)


def get_showable_lines(self) -> int:
    # if the text is longer than the possibly-to-display-lines, check which lines we show
    if self.showable_line_numbers_in_editor + self.showStartLine < self.maxLines:
        return self.showable_line_numbers_in_editor + self.showStartLine
    else:
        return self.maxLines


def render_background_objects(self) -> None:
    render_background_coloring(self)
    render_line_numbers(self)


def render_background_coloring(self) -> None:
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
                text = self.courier_font.render(get_line_number_string(x), 1, self.lineNumberColor)
                self.screen.blit(text, (self.editor_offset_X + 5, line_numbers_Y + 3))  # center of bg block

            line_numbers_Y += self.line_gap


def render_line_contents(self) -> None:
    """
    Called every frame. Renders all visible lines.
    Renders highlighted area and actual letters
    """
    # RENDERING 2 - Highlights
    # TODO - render while mouse is pressed, not only after dragged and dropped
    # TODO - calculate the correct area for the highlight
    # TODO - loop for highlighting multiple lines correctly
    if self.dragged_active:  # render highlighted area
        pygame.draw.rect(self.screen, (0, 0, 0), (
            self.drag_cursor_X_start, self.drag_cursor_Y_start, self.drag_cursor_X_end - self.drag_cursor_X_start,
            self.drag_cursor_Y_end - self.drag_cursor_Y_start + self.lineHeight))  # width, height

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


def render_caret(self) -> None:
    """
    Called every frame. Displays a cursor for x frames, then none for x frames.
    Dependent on FPS -> 5 intervalls per second
    Creates 'blinking' animation
    """
    self.Trenn_counter += 1
    if self.Trenn_counter > (self.FPS / 5) and self.caret_within_texteditor():


        self.screen.blit(self.trennzeichen_image, (self.cursor_X, self.cursor_Y))
        self.Trenn_counter = self.Trenn_counter % ((self.FPS / 5)*2)


def caret_within_texteditor(self) -> bool:
    """
    Tests whether the caret's coordinates are within the visible text area.
    If the caret can possibly be in a line which is not currently displayed after using the mouse wheel for scrolling.
    Test for 'self.editor_offset_Y <= self.cursor_Y' as the caret can have the exact same Y-coordinate as the offset if
    the caret is in the first line.
    """
    return self.editor_offset_X + self.lineNumberWidth < self.cursor_X < (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth) \
           and self.editor_offset_Y <= self.cursor_Y < (self.textAreaHeight + self.editor_offset_Y - self.conclusionBarHeight)


def reset_text_area_to_caret(self) -> None:
    """
    Reset visual area to include the line of caret if it is currently not visible. This function ensures
    that whenever we type, the line in which the caret resides is visible, even after scrolling.
    """

    if self.chosen_LineIndex < self.showStartLine:  # above visible area
        self.showStartLine = self.chosen_LineIndex
        self.rerenderLineNumbers = True
        self.update_caret_coordinates()
    elif self.chosen_LineIndex > (self.showStartLine + self.showable_line_numbers_in_editor - 1):  # below visible area
        self.showStartLine = self.chosen_LineIndex - self.showable_line_numbers_in_editor + 1
        self.rerenderLineNumbers = True
        self.update_caret_coordinates()
    # TODO: set cursor coordinates




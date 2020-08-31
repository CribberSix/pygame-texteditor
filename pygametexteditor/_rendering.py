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


def render_highlight(self, mouse_x, mouse_y) -> None:
    """
    Renders highlighted area:
    1. during drag-action (area follows mouse)
    2. after drag-action (area stays confined to selected area by drag_start / drag_end)
    """

    if self.dragged_active:  # area always starts at drag__start
        x1, y1 = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start, self.drag_chosen_LetterIndex_start)

        if self.dragged_finished:  # area confined by drag__end
            x2, y2 = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_end, self.drag_chosen_LetterIndex_end)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))

            # TODO: multi-line

        else:  # area follows mouse
            x2, y2 = self.get_rect_coord_from_mouse(mouse_x, mouse_y)
            if y1 == y2:  # single-line select
                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))
            else:
                # set the step pos/neg, depending whether the user highlights down- or upward
                step = self.lineHeight if y1 < y2 else self.lineHeight * (-1)
                for i, y in enumerate(range(y1, y2 + step, step)):  # for each line
                    # first line
                    if i == 0:
                        if y1 < y2:  # starting line < ending line
                            # Right sides highlight - drag_start until end
                            start_x, start_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start, self.drag_chosen_LetterIndex_start)
                            end_x, end_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start, len(self.line_String_array[self.drag_chosen_LineIndex_start]))
                            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(start_x, start_y, end_x - start_x, self.lineHeight))
                        else:  # starting line > ending line
                            # Left sided highlight - line-start until drag_start
                            end_x, end_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start, self.drag_chosen_LetterIndex_start)
                            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.xline_start, end_y, end_x - self.xline_start, self.lineHeight))
                    # middle lines
                    elif i < len(range(y1, y2 + step, step)) - 1:  # middle line
                        # Full highlight of entire line - start until end
                        lines = i if step > 0 else i * (-1)
                        end_x, end_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start + lines, len(self.line_String_array[self.drag_chosen_LineIndex_start + lines]))
                        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.xline_start, end_y, end_x - self.xline_start, self.lineHeight))

                    # last line
                    else:
                        if y1 < y2:  # starting line < ending line
                            # Left sided highlight - start to cursor (or start to end if cursor > end)
                            cursor_x, cursor_y = self.get_rect_coord_from_mouse(mouse_x, mouse_y)
                            end_x, end_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start + i, len(self.line_String_array[self.drag_chosen_LineIndex_start + i]))
                            # if cursor is behind a line, we can at max highlight until the last character
                            actual_x = end_x if cursor_x > end_x else cursor_x
                            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.xline_start, cursor_y, actual_x - self.xline_start, self.lineHeight))

                        else:  # starting line > ending line
                            # Right sided highlight - cursor to end  (or end to end if cursor > end)
                            cursor_x, cursor_y = self.get_rect_coord_from_mouse(mouse_x, mouse_y)
                            end_x, end_y = self.get_rect_coord_from_indizes(self.get_line_index(mouse_y), len(self.line_String_array[self.get_line_index(mouse_y)]))

                            if cursor_x > end_x:  # end to end = NONE
                                pass
                            else:  # cursor to end -> if cursor is within a line
                                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(cursor_x, cursor_y, end_x - cursor_x, self.lineHeight))


def get_rect_coord_from_mouse(self, mouse_x, mouse_y):
    line = self.get_line_index(mouse_y)
    letter = self.get_letter_index(mouse_x)
    return self.get_rect_coord_from_indizes(line, letter)


def get_rect_coord_from_indizes(self, line, letter) -> (int, int):
    line_coord = self.editor_offset_Y + (self.line_gap * (line - self.showStartLine))
    letter_coord = self.xline_start + (letter * self.letter_size_X)
    return letter_coord, line_coord


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




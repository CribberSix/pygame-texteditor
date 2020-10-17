import pygame


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
            if letter_end < 0:
                letter_end = 0
            self.highlight_lines(line_start, letter_start, line_end, letter_end)  # Actual highlighting

        else:  # active highlighting -> highlighted area follows mouse movements
            line_end = self.get_line_index(mouse_y)
            letter_end = self.get_letter_index(mouse_x)
            # adapt line_end: if mouse_y below showable area / existing lines,
            if line_end >= self.get_showable_lines():
                line_end = self.get_showable_lines() - 1  # select last showable/existing line as line_end

            # Correct letter_end based on cursor position / letters in the cursor's line
            if letter_end < 0:  # cursor is left of the line
                letter_end = 0
            elif letter_end > len(self.line_string_list[line_end]):
                letter_end = len(self.line_string_list[line_end])

            self.highlight_lines(line_start, letter_start, line_end, letter_end)  # Actual highlighting


def highlight_lines(self, line_start, letter_start, line_end, letter_end) -> None:
    """
    Highlights multiple lines based on indizies of starting & ending lines and letters.
    """
    if line_start == line_end:  # single-line highlight
        self.highlight_from_letter_to_letter(line_start, letter_start, letter_end)
    else:  # multi-line highlighting
        if line_start > line_end:  # swap variables based on up/downward highlight to make code more readable
            line_start, line_end = line_end, line_start
            letter_start, letter_end = letter_end, letter_start

        for i, line_number in enumerate(range(line_start, line_end + 1)):  # for each line
            if i == 0:  # first line
                self.highlight_from_letter_to_end(line_number, letter_start)  # right leaning highlight
            elif i < len(range(line_start, line_end)):  # middle line
                self.highlight_entire_line(line_number)
            else:  # last line
                self.highlight_from_start_to_letter(line_number, letter_end)  # left leaning highlight


def highlight_from_letter_to_end(self, line, letter) -> None:
    """
    Highlight from a specific letter by index to the end of a line.
    """
    if self.line_is_visible(line):
        x1, y1 = self.get_rect_coord_from_indizes(line, letter)
        x2, y2 = self.get_rect_coord_from_indizes(line, len(self.line_string_list[line]))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))


def highlight_from_start_to_letter(self, line, letter) -> None:
    """
    Highlight from the beginning of a line to a specific letter by index.
    """
    if self.line_is_visible(line):
        x1, y1 = self.get_rect_coord_from_indizes(line, 0)
        x2, y2 = self.get_rect_coord_from_indizes(line, letter)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))


def highlight_entire_line(self, line) -> None:
    """
    Full highlight of the entire line - first until last letter.
    """
    if self.line_is_visible(line):
        x1, y1 = self.get_rect_coord_from_indizes(line, 0)
        x2, y2 = self.get_rect_coord_from_indizes(line, len(self.line_string_list[line]))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))


def highlight_from_letter_to_letter(self, line, letter_start, letter_end) -> None:
    """
    Highlights within a single line from letter to letter by indizes.
    """
    if self.line_is_visible(line):
        x1, y1 = self.get_rect_coord_from_indizes(line, letter_start)
        x2, y2 = self.get_rect_coord_from_indizes(line, letter_end)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))

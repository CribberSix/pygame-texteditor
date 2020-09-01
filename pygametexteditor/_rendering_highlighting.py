import pygame


def highlight_from_start_to_dragstart(self) -> None:
    """
    Highlights the line starting at the first letter until the the drag_start point of the highlighting operation.
    (Differently put: From the drag_start point towards the left until the first letter.)
    """
    end_x, end_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start, self.drag_chosen_LetterIndex_start)
    pygame.draw.rect(self.screen, (0, 0, 0),
                     pygame.Rect(self.xline_start, end_y, end_x - self.xline_start, self.lineHeight))


def highlight_from_dragstart_to_end(self) -> None:
    """
    Highlights the line starting at the drag_start point of the highlighting operation towards the right
    until the end of the line.
    """
    start_x, start_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start, self.drag_chosen_LetterIndex_start)
    end_x, end_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start, len(self.line_String_array[self.drag_chosen_LineIndex_start]))
    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(start_x, start_y, end_x - start_x, self.lineHeight))


def highlight_entire_line(self, step, line_number) -> None:
    """
    Full highlight of entire line - first until last letter.
    Calculates in which line we are and in which direction we move (upward/downward highlighting) based on
    step (pos/neg) and the iteration of the highlighting algorithm.
    """
    lines = line_number if step > 0 else line_number * (-1)
    end_x, end_y = self.get_rect_coord_from_indizes(self.drag_chosen_LineIndex_start + lines, len(
        self.line_String_array[self.drag_chosen_LineIndex_start + lines]))
    pygame.draw.rect(self.screen, (0, 0, 0),
                     pygame.Rect(self.xline_start, end_y, end_x - self.xline_start, self.lineHeight))


def highlight_from_start_to_cursor(self, mouse_x, mouse_y) -> None:
    """
    # Left sided highlight - start to cursor (of cursor line)
    If the cursor is behind the last letter of the line, the entire line is highlighted
    """
    cursor_x, cursor_y = self.get_rect_coord_from_mouse(mouse_x, mouse_y)
    end_x, end_y = self.get_rect_coord_from_indizes(self.get_line_index(mouse_y),
                                                    len(self.line_String_array[self.get_line_index(mouse_y)]))
    # if cursor is behind a line, we can at max highlight until the last character
    actual_x = end_x if cursor_x > end_x else cursor_x
    pygame.draw.rect(self.screen, (0, 0, 0),
                     pygame.Rect(self.xline_start, cursor_y, actual_x - self.xline_start, self.lineHeight))


def highlight_from_cursor_to_end(self, mouse_x, mouse_y) -> None:
    """
    Right sided highlight - cursor to end (of cursor line)
    If the cursor is behind the last letter of the line, nothing is highlighted
    """
    cursor_x, cursor_y = self.get_rect_coord_from_mouse(mouse_x, mouse_y)
    end_x, end_y = self.get_rect_coord_from_indizes(self.get_line_index(mouse_y),
                                                    len(self.line_String_array[self.get_line_index(mouse_y)]))
    if cursor_x < end_x:
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(cursor_x, cursor_y, end_x - cursor_x, self.lineHeight))

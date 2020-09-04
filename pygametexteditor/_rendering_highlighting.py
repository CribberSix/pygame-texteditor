import pygame


def highlight_from_letter_to_end(self, line, letter) -> None:
    """
    Highlight from a specific letter by index to the end of a line.
    """
    x1, y1 = self.get_rect_coord_from_indizes(line, letter)
    x2, y2 = self.get_rect_coord_from_indizes(line, len(self.line_String_array[line]))
    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))


def highlight_from_start_to_letter(self, line, letter) -> None:
    """
    Highlight from the beginning of a line to a specific letter by index.
    """
    x1, y1 = self.get_rect_coord_from_indizes(line, 0)
    x2, y2 = self.get_rect_coord_from_indizes(line, letter)
    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))


def highlight_entire_line(self, line) -> None:
    """
    Full highlight of the entire line - first until last letter.
    """
    x1, y1 = self.get_rect_coord_from_indizes(line, 0)
    x2, y2 = self.get_rect_coord_from_indizes(line, len(self.line_String_array[line]))
    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))


def highlight_from_letter_to_letter(self, line, letter_start, letter_end) -> None:
    """
    Highlights within a single line from letter to letter by indizes.
    """
    x1, y1 = self.get_rect_coord_from_indizes(line, letter_start)
    x2, y2 = self.get_rect_coord_from_indizes(line, letter_end)
    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x1, y1, x2 - x1, self.lineHeight))


def highlight_lines(self, line_start, letter_start, line_end, letter_end) -> None:
    """
    Highlights multiple lines based on indizies of starting & ending lines and letters.
    """
    if line_start == line_end:  # single-line highlight
        self.highlight_from_letter_to_letter(line_start, letter_start, letter_end)
    else:  # fixed multi-line highlighting
        step = 1 if line_start < line_end else -1
        for i, line_number in enumerate(range(line_start, line_end + step, step)):  # for each line

            if i == 0:  # first line
                if line_start < line_end:
                    self.highlight_from_letter_to_end(line_number, letter_start)  # right leaning highlight
                else:
                    self.highlight_from_start_to_letter(line_number, letter_start)  # left leaning highlight

            elif i < len(range(line_start, line_end + step, step)) - 1:  # middle line
                self.highlight_entire_line(line_number)

            else:  # last line
                if line_start < line_end:
                    self.highlight_from_start_to_letter(line_number, letter_end)  # left leaning highlight
                else:
                    self.highlight_from_letter_to_end(line_number, letter_end)  # right leaning highlight

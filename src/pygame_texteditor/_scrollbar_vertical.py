import pygame


def render_scrollbar_vertical(self) -> None:
    self.display_scrollbar()


def display_scrollbar(self):
    # Scroll Bar
    if len(self.editor_lines) <= self.showable_line_numbers_in_editor:
        self.scrollbar = None
        return  # if scrollbar is not needed, don't show.

    # scroll bar is a fraction of the space
    w = self.scrollbar_width
    x = (
        self.editor_offset_x
        + self.editor_width
        - self.scrollbar_width
        - self.padding_between_edge_and_scrollbar
    )
    y = int(
        self.editor_offset_y
        + (self.scrollbar_width / 2)
        + (
            (self.editor_height - self.scrollbar_width)
            * ((self.first_showable_line_index * 1.0) / len(self.editor_lines))
        )
    )
    # Entire height minus the diameter as the ends are rounded. Multiplied with the fraction of displayable lines.
    h = int(
        (self.editor_height - (2 * self.scrollbar_width))
        * ((self.showable_line_numbers_in_editor * 1.0) / len(self.editor_lines))
    )
    self.scrollbar = pygame.Rect(x, y, w, h)

    pygame.draw.circle(
        self.screen, self.color_scrollbar, (int(x + (w / 2)), y), int(w / 2)
    )  # top round corner
    pygame.draw.rect(
        self.screen, self.color_scrollbar, self.scrollbar
    )  # actual scrollbar
    pygame.draw.circle(
        self.screen, self.color_scrollbar, (int(x + (w / 2)), y + h), int(w / 2)
    )  # bottom round corner


def scrollbar_up(self) -> None:
    self.first_showable_line_index -= 1
    self.caret_y += self.line_height_including_margin
    self.render_line_numbers_flag = True


def scrollbar_down(self) -> None:
    self.first_showable_line_index += 1
    self.caret_y -= self.line_height_including_margin
    self.render_line_numbers_flag = True

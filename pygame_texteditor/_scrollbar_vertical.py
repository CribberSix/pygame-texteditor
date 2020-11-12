import pygame


def render_scrollbar_vertical(self) -> None:
    self.display_scrollbar()


def display_scrollbar(self):
    # Scroll Bar

    if len(self.line_string_list) <= self.showable_line_numbers_in_editor:
        self.scrollbar = None
        return  # if scrollbar is not needed, don't show.

    # scroll bar is a fraction of the space
    w = self.scrollBarWidth 
    x = self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth - 2  # -2 for space between edge & scrollbar
    y = int(self.editor_offset_Y + (w/2) + (self.textAreaHeight * ((self.showStartLine * 1.0) / self.maxLines)))
    h = int((self.textAreaHeight - w) * ((self.showable_line_numbers_in_editor * 1.0) / self.maxLines))
    self.scrollbar = pygame.Rect(x, y, w, h)

    pygame.draw.circle(self.screen, self.color_scrollbar, (int(x + (w/2)), y), int(w/2))  # top round corner
    pygame.draw.rect(self.screen, self.color_scrollbar, self.scrollbar)  # actual scrollbar
    pygame.draw.circle(self.screen, self.color_scrollbar, (int(x + (w/2)), y + h), int(w/2))  # bottom round corner


def scrollbar_up(self) -> None:
    self.showStartLine -= 1
    self.cursor_Y += self.line_gap
    self.rerenderLineNumbers = True
    


def scrollbar_down(self) -> None:
    self.showStartLine += 1
    self.cursor_Y -= self.line_gap
    self.rerenderLineNumbers = True



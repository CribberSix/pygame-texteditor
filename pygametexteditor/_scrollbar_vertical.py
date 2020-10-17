import pygame


def render_scrollbar_vertical(self) -> None:
    self.display_background()
    self.display_scrollbuttons()
    self.display_scrollbar()


def display_background(self):
    x = self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth
    pygame.draw.rect(self.screen,
                     self.codingScrollBarBackgroundColor, (x, self.editor_offset_Y + self.scrollBarButtonHeight,
                                                           self.scrollBarWidth,
                                                           self.textAreaHeight - self.scrollBarButtonHeight * 2))


def display_scrollbar(self):
    # Scroll Bar
    if len(self.line_string_list) >= self.showable_line_numbers_in_editor:  # scroll bar is a fraction of the space
        self.scrollBarHeight = int((self.textAreaHeight - (2 * self.scrollBarButtonHeight)) * (
                    (self.showable_line_numbers_in_editor * 1.0) / self.maxLines))
    else:  # scrollbar fills the entire space
        self.scrollBarHeight = int((self.textAreaHeight - (2 * self.scrollBarButtonHeight)) * (
                    (self.showable_line_numbers_in_editor * 1.0) / self.showable_line_numbers_in_editor))

    self.scrollBarImg = pygame.transform.scale(self.scrollBarImg, (self.scrollBarWidth, self.scrollBarHeight))
    self.screen.blit(self.scrollBarImg, (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
                                         self.editor_offset_Y + self.scrollBarButtonHeight + int(
                                             (self.textAreaHeight - (2 * self.scrollBarButtonHeight)) * (
                                                         (self.showStartLine * 1.0) / (self.maxLines)))))


def display_scrollbuttons(self) -> None:
    """
    Displays the activated / deactivated button images
    :param self: pygame-texteditor instance
    :return: None
    """
    x = self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth
    y_up = self.editor_offset_Y
    y_down = self.editor_offset_Y + self.textAreaHeight - self.scrollBarButtonHeight

    # Logical buttons
    self.scroll_button(x, y_up, "ScrollUp")
    self.scroll_button(x, y_down, "ScrollDown")

    # Visual button representations
    # ____ UP
    if self.showStartLine == 0:  # can't scroll up -> deactivated button
        self.screen.blit(self.scrollUpButtonImg_Deactivated, (x, y_up))
    else:  # activated button
        self.screen.blit(self.scrollUpButtonImg, (x, y_up))

    # ____ DOWN
    if self.maxLines <= self.showStartLine + self.showable_line_numbers_in_editor:  # deactivated button
        self.screen.blit(self.scrollDownButtonImg_Deactivated, (x, y_down))
    else:  # activated button
        self.screen.blit(self.scrollDownButtonImg, (x, y_down))  # Scroll DownButton (active)


def scroll_button(self, x, y, action) -> None:
    # Description: Creates a button for rendering/blitting and offers action

    mouse = pygame.mouse.get_pos()
    # Mouse coordinates checking (on-button)
    if x + self.scrollBarWidth > mouse[0] > x and y + self.scrollBarWidth > mouse[1] > y and pygame.mouse.get_pressed()[0] == 1:
        pygame.time.delay(100)

        if action == "ScrollUp" and self.showStartLine > 0:
            self.scroll_up()
        elif action == "ScrollDown" and self.showStartLine + self.showable_line_numbers_in_editor < self.maxLines:
            self.scroll_down()
        self.rerenderLineNumbers = True
    else:
        pass    # Button is not clicked.


def scroll_up(self) -> None:
    self.showStartLine -= 1
    self.cursor_Y += self.line_gap
    self.rerenderLineNumbers = True


def scroll_down(self) -> None:
    self.showStartLine += 1
    self.cursor_Y -= self.line_gap
    self.rerenderLineNumbers = True



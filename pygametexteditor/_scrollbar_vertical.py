import pygame

def render_scrollbar_vertical(self):
    # _________RENDER_THE_SCROLLBAR_________#
    # Scrollbar Background
    pygame.draw.rect(self.screen, self.codingScrollBarBackgroundColor, (
    self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
    self.editor_offset_Y + self.scrollBarButtonHeight, self.scrollBarWidth,
    self.textAreaHeight - self.scrollBarButtonHeight * 2))  # Separator Coloring (below the coding area)
    # Scroll Buttons
    scrollButton(self, self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth, self.editor_offset_Y,
                      "ScrollUp")  # Scroll Up Button
    scrollButton(self, self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
                      self.editor_offset_Y + self.textAreaHeight - self.scrollBarButtonHeight,
                      "ScrollDown")  # Scroll Down Button
    # self.offset_X+self.textAreaWidth -self.scrollBarWidth, self.offset_Y + self.textAreaHeight - self.scrollBarButtonHeight
    # Scrollbar Buttons
    if self.showStartLine == 0:
        self.screen.blit(self.scrollUpButtonImg_Deactivated, (
        self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
        self.editor_offset_Y))  # Scroll Up (deactivated Button image)
    else:
        self.screen.blit(self.scrollUpButtonImg, (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
                                                  self.editor_offset_Y))  # Scroll Up Button (active)

    if self.maxLines <= self.showStartLine + self.showable_line_numbers_in_editor:
        self.screen.blit(self.scrollDownButtonImg_Deactivated, (
        self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
        self.editor_offset_Y + self.textAreaHeight - self.scrollBarButtonHeight))  # Scroll Down (deactivated Button image)
    else:
        self.screen.blit(self.scrollDownButtonImg, (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
           self.editor_offset_Y + self.textAreaHeight - self.scrollBarButtonHeight))  # Scroll DownButton (active)

    # Scroll Bar
    if len(self.line_String_array) >= self.showable_line_numbers_in_editor:
        self.scrollBarHeight = int((self.textAreaHeight - (2 * self.scrollBarButtonHeight)) * (
                    (self.showable_line_numbers_in_editor * 1.0) / self.maxLines))
    self.scrollBarImg = pygame.transform.scale(self.scrollBarImg, (self.scrollBarWidth, self.scrollBarHeight))
    self.screen.blit(self.scrollBarImg, (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth,
                                         self.editor_offset_Y + self.scrollBarButtonHeight + int(
                                             (self.textAreaHeight - (2 * self.scrollBarButtonHeight)) * (
                                                         (self.showStartLine * 1.0) / (self.maxLines)))))

def scrollButton(self, x, y, action):
    # Description: Creates a button for rendering/blitting and offers action

    mouse = pygame.mouse.get_pos()
    # Mouse coordinates checking (on-button)
    if x + self.scrollBarWidth > mouse[0] > x and y + self.scrollBarWidth > mouse[1] > y and pygame.mouse.get_pressed()[0] == 1:
        pygame.time.delay(100)
        # we dont want to click multiple times
        # TODO: replace with mod counter as counter does not hinder performance?

        if action == "ScrollUp" and self.showStartLine > 0:
            scrollUp(self)
        elif action == "ScrollDown" and self.showStartLine + self.showable_line_numbers_in_editor < self.maxLines:
            scrollDown(self)
        self.rerenderLineNumbers = True
    return None  # Button is not clicked.


def scrollUp(self):
    self.showStartLine -= 1
    self.cursor_Y += self.line_gap
    self.rerenderLineNumbers = True  # TODO: enhance performance - only rerender if necessary

def scrollDown(self):
    self.showStartLine += 1
    self.cursor_Y -= self.line_gap
    self.rerenderLineNumbers = True  # TODO: enhance performance - only rerender if necessary



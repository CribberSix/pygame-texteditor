import pygame


def get_line_number_string(num):
    if num < 10:  # 1-digit numbers
        return " " + str(num)
    else:  # 2-digit numbers
        return str(num)

def render_background_objects(self):
    render_background_coloring(self)
    render_line_numbers(self)

def render_background_coloring(self):
    bg_left = self.editor_offset_X + self.lineNumberWidth
    bg_top = self.editor_offset_Y
    bg_width = self.textAreaWidth - self.scrollBarWidth - self.lineNumberWidth
    bg_height = self.textAreaHeight
    pygame.draw.rect(self.screen, self.codingBackgroundColor, (bg_left, bg_top, bg_width, bg_height))

def get_showable_lines(self):
    # if the text is longer than the possibly-to-display-lines, check which lines we show
    if self.showable_line_numbers_in_editor + self.showStartLine < self.maxLines:
        return self.showable_line_numbers_in_editor + self.showStartLine
    else:
        return self.maxLines


def render_line_numbers(self):
    '''
    While background rendering is done for all "line-slots" (to overpaint remaining "old" numbers without lines)
    we render line-numbers only for existing string-lines.
    '''
    if self.displayLineNumbers and self.rerenderLineNumbers:
        self.rerenderLineNumbers = False
        line_numbers_Y = self.editor_offset_Y  # init for first line
        for x in range(self.showStartLine, self.showStartLine + self.showable_line_numbers_in_editor):

            # background
            pygame.draw.rect(self.screen, self.lineNumberBackgroundColor, (self.editor_offset_X, line_numbers_Y, self.lineNumberWidth, 17))
            # line number
            if x < get_showable_lines(self):
                text = self.courier_font.render(get_line_number_string(x), 1, self.lineNumberColor)
                self.screen.blit(text, (self.editor_offset_X + 5, line_numbers_Y + 3))  # center of bg block

            line_numbers_Y += self.line_gap

def render_line_contents(self):
    # TODO: Color-coding would be applied here #
    self.line_Text_array[self.chosen_LineIndex] = self.courier_font.render(self.line_String_array[self.chosen_LineIndex], 1, self.textColor)
    self.yline = self.yline_start

    first_line = self.showStartLine
    if self.showable_line_numbers_in_editor < len(self.line_Text_array):
        # we got more text than we are able to display
        last_line = self.showStartLine + self.showable_line_numbers_in_editor
    else:
        last_line = self.maxLines

    for line in self.line_Text_array[first_line: last_line]:
        self.screen.blit(line, (self.xline, self.yline))
        self.yline += self.line_gap

def render_cursor(self):
    '''
    Called every frame. Displays a cursor for 10 frames, then none for 10 frames.
    Creates 'blinking' animation
    '''
    self.Trenn_counter += 1
    if self.Trenn_counter > 10:
        self.screen.blit(self.trennzeichen_image, (self.cursor_X, self.cursor_Y))
        self.Trenn_counter = self.Trenn_counter % 20


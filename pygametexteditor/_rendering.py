import pygame


def get_rect_coord_from_mouse(self, mouse_x, mouse_y):
    """
    Return x and y pixel-coordinates for the position of the mouse.
    """
    line = self.get_line_index(mouse_y)
    letter = self.get_letter_index(mouse_x)
    return self.get_rect_coord_from_indizes(line, letter)


def get_rect_coord_from_indizes(self, line, letter) -> (int, int):
    """
    Return x and y pixel-coordinates for line and letter by index.
    """
    line_coord = self.editor_offset_Y + (self.line_gap * (line - self.showStartLine))
    letter_coord = self.xline_start + (letter * self.letter_size_X)
    return letter_coord, line_coord


def render_background_objects(self) -> None:
    """
    Renders background color of the text area.
    Renders line numbers if self.displayLineNumbers = True
    """
    render_background_coloring(self)
    render_line_numbers(self)


def render_background_coloring(self) -> None:
    """
    Renders background color of the text area.
    """
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
            if x < self.get_showable_lines():
                text = self.courier_font.render(str(x).zfill(2), 1, self.lineNumberColor)
                self.screen.blit(text, (self.editor_offset_X + 5, line_numbers_Y + 3))  # center of bg block

            line_numbers_Y += self.line_gap


def render_line_contents(self) -> None:
    """
    Called every frame. Updates the content of the surface of the line in which the cursor is.
    Renders all lines.
    Renders highlighted area and actual letters
    """

    # we only re-render the surface in which's line the cursor is currently -> better performance.
    # Limit render string of the current line, (TODO: shouldn't this be done to  all lines or is current one enough?)
    # so we don't blit outside of the textarea to the right
    render_length = int((self.textAreaWidth - self.lineNumberWidth - self.scrollBarWidth)/self.letter_size_X)
    render_string = self.line_String_array[self.chosen_LineIndex][:render_length]
    self.line_Text_array[self.chosen_LineIndex] = self.courier_font.render(render_string, 1, self.textColor)

    # render all visible lines once per Frame based on the visual array of surfaces.
    # Preparation of the rendering:
    self.yline = self.yline_start
    first_line = self.showStartLine
    if self.showable_line_numbers_in_editor < len(self.line_Text_array):
        # we got more text than we are able to display
        last_line = self.showStartLine + self.showable_line_numbers_in_editor
    else:
        last_line = self.maxLines

    # Actual line rendering
    for line in self.line_Text_array[first_line: last_line]:

        self.screen.blit(line, (self.xline, self.yline))
        self.yline += self.line_gap


def render_line_contents_syntax_coloring(self) -> None:
    """
    Rendering line contests with syntax coloring.
    We create a dict for every part of the line and include which letters are contained, the type and the color.
    So far implemented:
    - comments
    TODO:
    - quoted Strings
    - keywords
    - standalone - numbers
    """

    # Preparation of the rendering:
    self.yline = self.yline_start
    first_line = self.showStartLine
    if self.showable_line_numbers_in_editor < len(self.line_Text_array):
        # we got more text than we are able to display
        last_line = self.showStartLine + self.showable_line_numbers_in_editor
    else:
        last_line = self.maxLines

    # COLOR RENDERING START
    # For now, we recreate all of it every frame (!)
    rendering_list = []
    for line in self.line_Text_array:
        rendering_list.append([])  # create empty list for each line

    for i, line in enumerate(self.line_String_array):

        # SPLIT COMMENTS
        new_line = line.split('#', 1)  # split on first occurence
        rendering_list[i].append({'letters': new_line[0], 'type': 'letters', 'color': self.textColor})
        try:
            rendering_list[i].append({'letters': "#" + new_line[1], 'type': 'comment', 'color': self.textColor_comments})
        except IndexError:
            pass  # no comments found in this line

        # TODO: SPLIT ON QUOTES
        

    # Actual line rendering based on dict-keys
    for line_array in rendering_list[first_line: last_line]:
        xcoord = self.xline_start
        for part in line_array:
            surface = self.courier_font.render(part['letters'], 1, part['color'])
            self.screen.blit(surface, (xcoord, self.yline))

            xcoord = xcoord+ (len(part['letters']) * self.letter_size_X)  # next line-part prep
        self.yline += self.line_gap  # next line prep


    #self.textColor = (171, 178, 191)  # (171, 178, 191)

    #self.line_Text_array[self.chosen_LineIndex] = self.courier_font.render(render_string, 1, self.textColor)

    #self.line_Text_array.append(self.courier_font.render(new_line[0], 1, (160, 160, 160)))

    # create a surface based on spacebars
    # new_line = [e+" " for e in line.split(" ") if e]





def caret_within_texteditor(self) -> bool:
    """
    Tests whether the caret's coordinates are within the visible text area.
    If the caret can possibly be in a line which is not currently displayed after using the mouse wheel for scrolling.
    Test for 'self.editor_offset_Y <= self.cursor_Y' as the caret can have the exact same Y-coordinate as the offset if
    the caret is in the first line.
    """
    return self.editor_offset_X + self.lineNumberWidth < self.cursor_X < (
                self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth) \
           and self.editor_offset_Y <= self.cursor_Y < (
                       self.textAreaHeight + self.editor_offset_Y - self.conclusionBarHeight)


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
        self.Trenn_counter = self.Trenn_counter % ((self.FPS / 5) * 2)


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

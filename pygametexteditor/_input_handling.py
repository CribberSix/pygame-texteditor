import pygame
from sys import exit
from ._scrollbar_vertical import scrollDown, scrollUp


def mouse_within_texteditor(self, mouse_x, mouse_y):
    return self.editor_offset_X + self.lineNumberWidth < mouse_x < (self.editor_offset_X + self.textAreaWidth - self.scrollBarWidth) \
           and self.editor_offset_Y < mouse_y < (self.textAreaHeight + self.editor_offset_Y - self.conclusionBarHeight)


def mouse_within_existing_lines(self, mouse_y):
    return mouse_y < self.editor_offset_Y + (self.lineHeight * self.maxLines)


def get_line_index(self, mouse_y):
    return int(((mouse_y - self.editor_offset_Y) / self.line_gap) + (self.showStartLine))


def get_letter_index(self, mouse_x):
    return int((mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)


def get_number_of_letters_in_line_by_mouse(self, mouse_y):
    line_index = get_line_index(self, mouse_y)
    return get_number_of_letters_in_line_by_index(self, line_index)


def get_number_of_letters_in_line_by_index(self, index):
    return len(self.line_String_array[index])


def set_cursor_x_position(self, mouse_x, mouse_y):
    # end of line
    if get_number_of_letters_in_line_by_mouse(self, mouse_y) < get_letter_index(self, mouse_x):
        self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])
        self.drag_cursor_X_start = self.xline_start + (
                len(self.line_String_array[self.drag_chosen_LineIndex_start]) * self.letter_size_X)
    # within existing line
    else:
        self.drag_chosen_LetterIndex_start = int(
            (mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)
        self.drag_cursor_X_start = self.editor_offset_X + self.xline_start_offset + (
                self.drag_chosen_LetterIndex_start * self.letter_size_X)
    print("self.drag_chosen_LetterIndex_start: " + str(self.drag_chosen_LetterIndex_start))


def set_cursor_y_position(self, mouse_y):
    self.drag_chosen_LineIndex_start = get_line_index(self, mouse_y)
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap) - (
                self.showStartLine * self.lineHeight)
    print("self.drag_chosen_LineIndex_start: " + str(self.drag_chosen_LineIndex_start))


def set_cursor_after_last_line(self):
    self.drag_chosen_LineIndex_start = self.maxLines - 1  # go to the end of the last line
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap)
    # Last letter of the line
    self.drag_chosen_LetterIndex_start = get_number_of_letters_in_line_by_index(self, self.drag_chosen_LineIndex_start)
    self.drag_cursor_X_start = self.editor_offset_X + self.xline_start_offset + (
                self.drag_chosen_LetterIndex_start * self.letter_size_X)


def mouse_inside_text_area(self, mouse_x, mouse_y):
    return self.editor_offset_X < mouse_x < self.editor_offset_X + self.textAreaWidth \
           and self.editor_offset_Y < mouse_y < self.editor_offset_Y + self.textAreaHeight


def handle_keyboard_input(self, mouse_x, mouse_y):
    self.deleteCounter += 1
    self.deleteCounter = self.deleteCounter % 2
    # TODO: find a good option here. If FPS_max = 30; then we can delete 15 characters each second

    # Detect tapping/holding of the "DELETE" and "BACKSPACE" key
    Xkeys = pygame.key.get_pressed()
    if Xkeys[pygame.K_DELETE] and self.deleteCounter == 0:
        self.handle_keyboard_delete()
    if Xkeys[pygame.K_BACKSPACE] and self.deleteCounter == 0:
        self.handle_keyboard_backspace()

    # ALL OTHER KEYS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Fixes the bug that pygame takes up space in the RAM when game is just closed by sys.exit()
            exit()

        # ___ MOUSE SCROLLING ___ #
        # Mouse scrolling wheel should only work if it is within the coding area.
        if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_within_texteditor(mouse_x, mouse_y):
            if event.button == 4 and self.showStartLine > 0:
                scrollUp(self)
            elif event.button == 5 and self.showStartLine + self.showable_line_numbers_in_editor < self.maxLines:
                scrollDown(self)
            elif event.button == 1:  # left mouse button
                if not self.click_hold:
                    self.last_clickdown_cycle = self.cycleCounter
                    self.click_hold = True  # in order not to have the mouse move around after a click, we need to disable this function until we RELEASE it.
                    if self.mouse_within_texteditor(mouse_x, mouse_y):
                        if mouse_within_existing_lines(self, mouse_y):
                            set_cursor_y_position(self, mouse_y)
                            set_cursor_x_position(self, mouse_x, mouse_y)
                        else:  # clicked below the existing lines
                            set_cursor_after_last_line(self)

        # ___ MOUSE DRAGGING ___ #
        # MOUSEBUTTONDOWN is handled previously in the mouse input.
        if event.type == pygame.MOUSEBUTTONUP:
            self.last_clickup_cycle = self.cycleCounter
            self.click_hold = False

            if self.mouse_inside_text_area(mouse_x, mouse_y):  # check if I let go inside the text area
                if mouse_y < self.editor_offset_Y + (self.lineHeight * self.maxLines):  # click in existing lines
                    # Choose Line (y-axis)
                    self.drag_chosen_LineIndex_end = int(
                        ((mouse_y - self.editor_offset_Y) / self.line_gap) + self.showStartLine)
                    self.drag_cursor_Y_end = self.editor_offset_Y + (self.drag_chosen_LineIndex_end * self.line_gap) - (
                                self.showStartLine * self.lineHeight)
                    # Choose Letter (x-axis)
                    prep_LetterIndex_drag = int((
                                                            mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)  # cast as integer as we use it as index

                    # check if clicked behind the end of a line
                    if len(self.line_String_array[
                               self.drag_chosen_LineIndex_end]) < prep_LetterIndex_drag:  # end of line
                        self.drag_chosen_LetterIndex_end = len(self.line_String_array[self.drag_chosen_LineIndex_end])
                        self.drag_cursor_X_end = self.xline_start + (
                                    len(self.line_String_array[self.drag_chosen_LineIndex_end]) * self.letter_size_X)
                    else:  # within existing line
                        self.drag_chosen_LetterIndex_end = int((
                                                                           mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)  # cast as integer as we use it as index
                        self.drag_cursor_X_end = self.editor_offset_X + self.xline_start_offset + (
                                    self.drag_chosen_LetterIndex_end * self.letter_size_X)

                else:  # clicked beneath the existing lines
                    #  go to the end of the last line.
                    self.chosen_LineIndex = self.maxLines - 1
                    self.drag_cursor_Y_end = self.editor_offset_Y + (self.drag_chosen_LineIndex_end * self.line_gap)
                    # Last letter of the line
                    self.drag_chosen_LetterIndex_end = len(self.line_String_array[self.drag_chosen_LineIndex_end])
                    self.drag_cursor_X_end = self.editor_offset_X + self.xline_start_offset + (
                            self.drag_chosen_LetterIndex_end * self.letter_size_X)

        # _______ CHECK FOR MOUSE DRAG AND HANDLE CLICK _______ #
        if (self.last_clickup_cycle - self.last_clickdown_cycle) >= 0:
            # clicked the mouse lately and has not been handled yet.
            # we dont have to check how long the mouse was held, to differentiate between click and drag
            # but if the down click is on the same letter and line as the upclick!!!
            if self.drag_chosen_LineIndex_end == self.drag_chosen_LineIndex_start and self.drag_chosen_LetterIndex_end == self.drag_chosen_LetterIndex_start:
                self.chosen_LineIndex = self.drag_chosen_LineIndex_end
                self.chosen_LetterIndex = self.drag_chosen_LetterIndex_end
                self.cursor_X = self.drag_cursor_X_end
                self.cursor_Y = self.drag_cursor_Y_end
            else:
                self.dragged_active = True
                self.cursor_X = self.drag_cursor_X_end
                self.cursor_Y = self.drag_cursor_Y_end

            # reset after upclick => difference is "-1" and hence smaller than 0. Wait for next clickup.
            self.last_clickup_cycle = -1
            self.last_clickdown_cycle = 0

        if event.type == pygame.KEYDOWN and self.dragged_active:
            # TODO: if we type a letter / return / backspace / del we delete the marked area.
            # TODO: if we type an arrow we jump in front of or at the backend of the area.
            # print("Something with mouse dragging should be happening here.")
            pass

        # ___ KEYS ___ #
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)  # Returns string id of pressed key.
            if len(key) == 1:  # This covers all letters and numbers not on numpad.
                self.chosen_LetterIndex = int(self.chosen_LetterIndex)
                self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][
                                                                :self.chosen_LetterIndex] + event.unicode + \
                                                                self.line_String_array[self.chosen_LineIndex][
                                                                self.chosen_LetterIndex:]
                self.cursor_X += self.letter_size_X
                self.chosen_LetterIndex += 1

            elif event.key == pygame.K_TAB:  # ___TABULATOR
                self.handle_keyboard_tab()
            elif event.key == pygame.K_SPACE:  # ___SPACEBAR
                self.handle_keyboard_space()
            elif event.key == pygame.K_RETURN:  # ___RETURN
                self.handle_keyboard_return()
            elif event.key == pygame.K_UP and self.chosen_LineIndex > 0:  # ___ARROW_UP
               self.handle_keyboard_arrow_up()
            elif event.key == pygame.K_DOWN:  # ___ARROW_DOWN
                self.handle_keyboard_arrow_down()
            elif event.key == pygame.K_RIGHT:  # ___ARROW_RIGHT
                self.handle_keyboard_arrow_right()
            elif event.key == pygame.K_LEFT:  # ___ARROW_LEFT
                self.handle_keyboard_arrow_left()
            else:
                if event.key not in [pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_DELETE,
                                     pygame.K_BACKSPACE]:  # we handled those separately
                    raise ValueError("Key not binded: " + str(pygame.key.name(event.key)))


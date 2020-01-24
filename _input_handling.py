import pygame

def get_showable_lines(self):
    # if the text is longer than the possibly-to-display-lines, check which lines we show
    if self.showable_line_numbers_in_editor + self.showStartLine < self.maxLines:
        return self.showable_line_numbers_in_editor + self.showStartLine
    else:
        return self.maxLines


def get_line_number_string(self, num):
    if num < 10:  # 1-digit numbers
        return " " + str(num)
    else:  # 2-digit numbers
        return str(num)


def check_if_mouse_within_texteditor(self, mouse_x, mouse_y):
    return (mouse_x > self.editor_offset_X + self.lineNumberWidth) and (
            mouse_x < (self.editor_offset_X + self.codingAreaWidth - self.scrollBarWidth)) and (
                   mouse_y > self.editor_offset_Y) and (
                   mouse_y < (self.codingAreaHeight + self.editor_offset_Y - self.conclusionBarHeight))


def check_if_mouse_within_existing_lines(self, mouse_y):
    return mouse_y < self.editor_offset_Y + (self.lineHeight * self.maxLines)


def get_line_index(self, mouse_y):
    return int(((mouse_y - self.editor_offset_Y) / self.line_gap) + (self.showStartLine))


def get_letter_index(self, mouse_x):
    return int((mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)


def get_number_of_letters_in_line_by_mouse(self, mouse_y):
    line_index = self.get_line_index(mouse_y)
    return self.get_number_of_letters_in_line_by_index(line_index)


def get_number_of_letters_in_line_by_index(self, index):
    return len(self.line_String_array[index])


def set_cursor_x_position(self, mouse_x, mouse_y):
    # end of line
    if self.get_number_of_letters_in_line_by_mouse(mouse_y) < self.get_letter_index(mouse_x):
        self.drag_chosen_LetterIndex_start = len(self.line_String_array[self.drag_chosen_LineIndex_start])
        self.drag_cursor_X_start = self.xline_start + (
                len(self.line_String_array[self.drag_chosen_LineIndex_start]) * self.letter_size_X)
    # within existing line
    else:
        self.drag_chosen_LetterIndex_start = int(
            (mouse_x - self.editor_offset_X - self.xline_start_offset) / self.letter_size_X)
        self.drag_cursor_X_start = self.editor_offset_X + self.xline_start_offset + (
                self.drag_chosen_LetterIndex_start * self.letter_size_X)


def set_cursor_y_position(self, mouse_y):
    self.drag_chosen_LineIndex_start = self.get_line_index(mouse_y)
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap) - (
                self.showStartLine * self.lineHeight)


def set_cursor_after_last_line(self, mouse_y):
    self.drag_chosen_LineIndex_start = self.maxLines - 1  # go to the end of the last line
    self.drag_cursor_Y_start = self.editor_offset_Y + (self.drag_chosen_LineIndex_start * self.line_gap)
    # Last letter of the line
    self.drag_chosen_LetterIndex_start = self.get_number_of_letters_in_line_by_index(self.drag_chosen_LineIndex_start)
    self.drag_cursor_X_start = self.editor_offset_X + self.xline_start_offset + (
                self.drag_chosen_LetterIndex_start * self.letter_size_X)


def handle_input_mouse_clicks(self, mouse_x, mouse_y):
    # Mouse clicks
    click = pygame.mouse.get_pressed()
    if click[0] and not self.click_hold:  # left click and is not already being held
        self.last_clickdown_cycle = self.cycleCounter
        self.click_hold = True  # in order not to have the mouse move around after a click, we need to disable this function until we RELEASE it.
        if self.check_if_mouse_within_texteditor(mouse_x, mouse_y):
            if self.check_if_mouse_within_existing_lines(mouse_y):
                self.set_cursor_y_position(mouse_y)
                self.set_cursor_x_position(mouse_x, mouse_y)
            else:  # clicked below the existing lines
                self.set_cursor_after_last_line(mouse_y)


def handle_keyboard_input(self, mouse_x, mouse_y):
    self.deleteCounter += 1
    self.deleteCounter = self.deleteCounter % 2  # TODO: find a good option here. If FPS_max = 30; then we can delete 15 characters each second

    # Detect tapping/holding of the "DELETE" and "BACKSPACE" key
    Xkeys = pygame.key.get_pressed()
    if Xkeys[pygame.K_DELETE] and self.deleteCounter == 0:
        if self.chosen_LetterIndex == len(
                self.line_String_array[self.chosen_LineIndex]):  # End of a line  (choose next line)
            if self.chosen_LineIndex != (
                    self.maxLines - 1):  # NOT in the last line &(prev) at the end of the line, I cannot delete anything
                self.line_String_array[self.chosen_LineIndex] += self.line_String_array[
                    self.chosen_LineIndex + 1]  # add the contents of the next line to the current one
                self.line_String_array.pop(
                    self.chosen_LineIndex + 1)  # delete the Strings-line in order to move the following lines one upwards
                self.maxLines -= 1  # Keep the variable aligned
                self.line_Text_array.pop(
                    self.chosen_LineIndex + 1)  # delete the Text-line in order to move the following lines one upwards
                self.rerenderLineNumbers = True
                if self.showStartLine > 0:
                    if (
                            self.showStartLine + self.showable_line_numbers_in_editor) > self.maxLines:  # The scrollbar is all the way down. We delete a line, so we have to "pull everything one visual line down"
                        self.showStartLine -= 1  # "pull one visual line down" (array-based)
                        self.cursor_Y += self.line_gap  # move the curser one down.  (visually based)

        elif self.chosen_LetterIndex < (
        len(self.line_String_array[self.chosen_LineIndex])):  # mid-line (Cursor stays on point)
            self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][
                                                            :(self.chosen_LetterIndex)] + self.line_String_array[
                                                                                              self.chosen_LineIndex][(
                                                                                                                                 self.chosen_LetterIndex + 1):]

    if Xkeys[pygame.K_BACKSPACE] and self.deleteCounter == 0:
        self.chosen_LetterIndex = int(self.chosen_LetterIndex)
        if self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:  # One Line back if at X-Position 0 and not in the first Line
            # Line & Letter Handling
            self.chosen_LineIndex -= 1
            self.cursor_Y -= self.line_gap
            self.cursor_X = self.xline_start + (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)
            self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
            self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] + \
                                                            self.line_String_array[
                                                                self.chosen_LineIndex + 1]  # take the rest of the line into the previous line
            self.line_String_array.pop(
                self.chosen_LineIndex + 1)  # delete the Strings-line in order to move the following lines one upwards
            self.maxLines -= 1  # Keep the variable aligned
            self.line_Text_array.pop(
                self.chosen_LineIndex + 1)  # delete the Text-line in order to move the following lines one upwards
            self.rerenderLineNumbers = True
            # Scroll Handling
            if self.showStartLine > 0:
                if (
                        self.showStartLine + self.showable_line_numbers_in_editor) > self.maxLines:  # The scrollbar is all the way down. We delete a line, so we have to "pull everything one visual line down"
                    self.showStartLine -= 1  # "pull one visual line down" (array-based)
                    self.cursor_Y += self.line_gap  # move the curser one down.  (visually based)
            if self.chosen_LineIndex == (
                    self.showStartLine - 1):  # Im in the first rendered line (but NOT  the "0" line) and at the beginning of the line. => move one upward, change showstartLine & cursor placement.
                self.showStartLine -= 1
                self.cursor_Y += self.line_gap

        elif self.chosen_LetterIndex > 0:  # Else: mid-lineDelete a letter (but only if there are letters left) (Cursor moves)
            self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][
                                                            :(self.chosen_LetterIndex - 1)] + self.line_String_array[
                                                                                                  self.chosen_LineIndex][
                                                                                              (
                                                                                                  self.chosen_LetterIndex):]
            self.cursor_X -= self.letter_size_X
            self.chosen_LetterIndex -= 1

    # ALL OTHER KEYS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Fixes the bug that pygame takes up space in the RAM when game is just closed by sys.exit()
            sys.exit()

        # ___ MOUSE SCROLLING ___ #
        # Mouse scrolling wheel should only work if it is within the coding area.
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_x > self.editor_offset_X and mouse_x < self.editor_offset_X + self.codingAreaWidth and mouse_y > self.editor_offset_Y and mouse_y < self.editor_offset_Y + self.codingAreaHeight:
            if event.button == 4 and self.showStartLine > 0:
                self.scrollUp()
            elif event.button == 5 and self.showStartLine + self.showable_line_numbers_in_editor < self.maxLines:
                self.scrollDown()

        # ___ MOUSE DRAGGING ___ #
        # MOUSEBUTTONDOWN is handled previously in the mouse input.
        if event.type == pygame.MOUSEBUTTONUP:
            self.last_clickup_cycle = self.cycleCounter
            self.click_hold = False
            # check if I clicked into the text area:
            if (mouse_x > self.editor_offset_X + self.lineNumberWidth) and (
                    mouse_x < (self.editor_offset_X + self.codingAreaWidth - self.scrollBarWidth)) and (
                    mouse_y > self.editor_offset_Y) and (
                    mouse_y < (self.codingAreaHeight + self.editor_offset_Y - self.conclusionBarHeight)):

                # Check if I clicked into the existing Lines
                if (mouse_y < self.editor_offset_Y + (
                        self.lineHeight * self.maxLines)):  # clicked INTO the existing lines.
                    # Choose Line (y-axis)
                    self.drag_chosen_LineIndex_end = int(
                        ((mouse_y - self.editor_offset_Y) / self.line_gap) + (self.showStartLine))
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
        if (
                self.last_clickup_cycle - self.last_clickdown_cycle) >= 0:  # clicked the mouse lately and has not been handled yet.
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

            # ___TABULATOR
            elif key == "tab":
                self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][
                                                                :self.chosen_LetterIndex] + "    " + \
                                                                self.line_String_array[self.chosen_LineIndex][
                                                                self.chosen_LetterIndex:]
                self.cursor_X += self.letter_size_X * 4
                self.chosen_LetterIndex += 4

            # ___SPACEBAR
            elif key == "space":
                self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][
                                                                :self.chosen_LetterIndex] + " " + \
                                                                self.line_String_array[self.chosen_LineIndex][
                                                                self.chosen_LetterIndex:]
                self.cursor_X += self.letter_size_X
                self.chosen_LetterIndex += 1

            # ___ARROW_UP
            elif event.key == pygame.K_UP and self.chosen_LineIndex > 0:
                self.chosen_LineIndex -= 1
                self.cursor_Y -= self.line_gap
                if len(self.line_String_array[
                           self.chosen_LineIndex]) < self.chosen_LetterIndex:  # have to reset (toward the left)
                    self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
                    self.cursor_X = (len(
                        self.line_String_array[self.chosen_LineIndex])) * self.letter_size_X + self.xline_start
                if self.chosen_LineIndex < self.showStartLine:
                    self.showStartLine -= 1
                    self.cursor_Y += self.line_gap
                    self.rerenderLineNumbers = True

            # ___ARROW_DOWN
            elif event.key == pygame.K_DOWN:
                if (self.chosen_LineIndex < self.maxLines - 1):  # Not in the last line, i can move downward.
                    self.chosen_LineIndex += 1
                    self.cursor_Y += self.line_gap
                    if len(self.line_String_array[self.chosen_LineIndex]) < self.chosen_LetterIndex:
                        self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
                        self.cursor_X = ((len(
                            self.line_String_array[self.chosen_LineIndex])) * self.letter_size_X) + self.xline_start
                    if self.chosen_LineIndex > (
                            self.showStartLine + self.showable_line_numbers_in_editor - 1):  # I move downward outside of the rendered lines => "pull the lines up"
                        self.showStartLine += 1
                        self.cursor_Y -= self.line_gap
                        self.rerenderLineNumbers = True
                if (self.chosen_LineIndex == self.maxLines - 1):  # im in the last line and want to jump to its end.
                    self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])  # end of the line
                    self.cursor_X = self.xline_start + (
                                len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)

            # ___ARROW_RIGHT
            elif event.key == pygame.K_RIGHT:
                if self.chosen_LetterIndex < (len(self.line_String_array[self.chosen_LineIndex])):  # mid-line
                    self.chosen_LetterIndex += 1
                    self.cursor_X += self.letter_size_X
                elif self.chosen_LetterIndex == len(self.line_String_array[self.chosen_LineIndex]) and not (
                        self.chosen_LineIndex == (
                        self.maxLines - 1)):  # end of line => move over into the start of the next lint
                    self.chosen_LetterIndex = 0
                    self.chosen_LineIndex += 1
                    self.cursor_X = self.xline_start
                    self.cursor_Y += self.line_gap
                    if self.chosen_LineIndex > (
                            self.showStartLine + self.showable_line_numbers_in_editor - 1):  # I move downward outside of the rendered lines => "pull the lines up"
                        self.showStartLine += 1
                        self.cursor_Y -= self.line_gap
                        self.rerenderLineNumbers = True

            # ___ARROW_LEFT
            elif event.key == pygame.K_LEFT:
                if self.chosen_LetterIndex > 0:  # mid-line
                    self.chosen_LetterIndex -= 1
                    self.cursor_X -= self.letter_size_X
                elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:  # Move over into previous Line (if there is any)
                    self.chosen_LineIndex -= 1
                    self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])  # end of previous line
                    self.cursor_X = self.xline_start + (
                                len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)
                    self.cursor_Y -= self.line_gap
                    if self.chosen_LineIndex < self.showStartLine:
                        self.showStartLine -= 1
                        self.cursor_Y += self.line_gap
                        self.rerenderLineNumbers = True

            # ___RETURN
            elif event.key == pygame.K_RETURN:
                transferString = self.line_String_array[self.chosen_LineIndex][
                                 (self.chosen_LetterIndex):]  # Transfer letters behind cursor to next line
                self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][
                                                                :self.chosen_LetterIndex]  # Edit previous line
                self.line_Text_array[self.chosen_LineIndex] = self.Courier_Text_15.render(
                    self.line_String_array[self.chosen_LineIndex], 1, self.textColor)  # formatting the line
                self.chosen_LineIndex += 1
                self.chosen_LetterIndex = 0
                self.maxLines += 1
                self.cursor_X = self.xline_start
                self.line_String_array.insert(self.chosen_LineIndex, "")
                self.line_Text_array.insert(self.chosen_LineIndex, self.Courier_Text_15.render("", 1, (10, 10, 10)))
                self.line_String_array[self.chosen_LineIndex] = self.line_String_array[
                                                                    self.chosen_LineIndex] + transferString  # EDIT new line with transfer letters
                self.rerenderLineNumbers = True

                if self.chosen_LineIndex > (self.showable_line_numbers_in_editor - 1):  # Last row
                    self.showStartLine += 1
                else:
                    self.cursor_Y += self.line_gap  # not in last row, put curser one line down.
            else:
                if event.key not in [pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_DELETE,
                                     pygame.K_BACKSPACE]:  # we handled those separately
                    print("Key outside scope: " + str(pygame.key.name(event.key)))

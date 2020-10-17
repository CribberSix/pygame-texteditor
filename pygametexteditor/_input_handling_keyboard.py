import pygame


def handle_keyboard_input(self, pygame_events, pressed_keys) -> None:

    if self.deleteCounter > 0:
        self.deleteCounter -= 1
    #self.deleteCounter = self.deleteCounter % 5  # If FPS = 60; then we can delete 12 characters each second


    # Detect tapping/holding of the "DELETE" and "BACKSPACE" key
    if self.dragged_finished and self.dragged_active and \
            (pressed_keys[pygame.K_DELETE] or pressed_keys[pygame.K_BACKSPACE]):
        delete_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DELETE)  # create the event
        self.handle_input_with_highlight(delete_event)  # delete and backspace have the same functionality
        self.deleteCounter = 5
    elif pressed_keys[pygame.K_DELETE] and self.deleteCounter == 0:
        self.handle_keyboard_delete()  # handle input
        self.reset_text_area_to_caret()  # reset caret if necessary
        self.deleteCounter = 5
    elif pressed_keys[pygame.K_BACKSPACE] and self.deleteCounter == 0:
        self.handle_keyboard_backspace()  # handle input
        self.reset_text_area_to_caret()  # reset caret if necessary
        self.deleteCounter = 5

    # ___ OTHER KEYS ___ #
    for event in pygame_events:
        if event.type == pygame.KEYDOWN:

            # ___ COMBINATION KEYS ___
            # Can be applied whether something is highlighted or not!
            if (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]) and event.key == pygame.K_a:
                self.highlight_all()
            elif (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]) and event.key == pygame.K_v:
                self.handle_highlight_and_paste()

            elif self.dragged_finished and self.dragged_active:
                # Only work if something is highlighted!
                if (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]) and event.key == pygame.K_x:
                    self.handle_highlight_and_cut()
                elif (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]) and event.key == pygame.K_c:
                    self.handle_highlight_and_copy()
                else:
                    self.handle_input_with_highlight(event)  # handle char input on highlight

            else:
                self.reset_text_area_to_caret()  # reset visual area to include line of caret if necessaryss

                # ___ NORMAL KEYS ___
                if len(pygame.key.name(event.key)) == 1:  # This covers all letters and numbers (not on numpad).
                    self.chosen_LetterIndex = int(self.chosen_LetterIndex)
                    self.insert_unicode(event.unicode)
                # ___ SPECIAL KEYS ___
                elif event.key == pygame.K_TAB:  # ___TABULATOR
                    self.handle_keyboard_tab()
                elif event.key == pygame.K_SPACE:  # ___SPACEBAR
                    self.handle_keyboard_space()
                elif event.key == pygame.K_RETURN:  # ___RETURN
                    self.handle_keyboard_return()
                elif event.key == pygame.K_UP:  # ___ARROW_UP
                    self.handle_keyboard_arrow_up()
                elif event.key == pygame.K_DOWN:  # ___ARROW_DOWN
                    self.handle_keyboard_arrow_down()
                elif event.key == pygame.K_RIGHT:  # ___ARROW_RIGHT
                    self.handle_keyboard_arrow_right()
                elif event.key == pygame.K_LEFT:  # ___ARROW_LEFT
                    self.handle_keyboard_arrow_left()


                else:
                    if event.key not in [pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_DELETE,
                                         pygame.K_BACKSPACE, pygame.K_CAPSLOCK, pygame.K_LCTRL, pygame.K_RCTRL]:
                        # We handled the keys separately
                        # Capslock is apparently implicitly handled when using it in combination

                        # disabled for smooth development:
                        # raise ValueError("No key implementation: " + str(pygame.key.name(event.key)))
                        print("No key implementation: " + str(pygame.key.name(event.key)))


def insert_unicode(self, unicode) -> None:
    self.line_string_list[self.chosen_LineIndex] = self.line_string_list[self.chosen_LineIndex][
                                                    :self.chosen_LetterIndex] + unicode + \
                                                    self.line_string_list[self.chosen_LineIndex][
                                                    self.chosen_LetterIndex:]
    self.cursor_X += self.letter_size_X
    self.chosen_LetterIndex += 1


def handle_keyboard_backspace(self) -> None:
    if self.chosen_LetterIndex == 0 and self.chosen_LineIndex == 0:
        # First position and in the first Line -> nothing happens
        pass
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:
        # One Line back if at X-Position 0 and not in the first Line

        # set letter and line index to newly current line
        self.chosen_LineIndex -= 1
        self.chosen_LetterIndex = len(self.line_string_list[self.chosen_LineIndex])
        # set visual cursor one line above and at the end of the line
        self.cursor_Y -= self.line_gap
        self.cursor_X = self.xline_start + (len(self.line_string_list[self.chosen_LineIndex]) * self.letter_size_X)

        # take the rest of the former line into the current line
        self.line_string_list[self.chosen_LineIndex] = self.line_string_list[self.chosen_LineIndex] + \
            self.line_string_list[self.chosen_LineIndex + 1]

        # delete the former line
        # LOGICAL lines
        self.line_string_list.pop(self.chosen_LineIndex + 1)
        self.maxLines -= 1
        # VISUAL lines
        self.rerenderLineNumbers = True

        # Handling of the resulting scrolling functionality of removing one line
        if self.showStartLine > 0:
            if (self.showStartLine + self.showable_line_numbers_in_editor) > self.maxLines:
                # The scrollbar is all the way down. We delete a line,
                # so we have to "pull everything one visual line down"
                self.showStartLine -= 1  # "pull one visual line down" (array-based)
                self.cursor_Y += self.line_gap  # move the curser one down.  (visually based)
        if self.chosen_LineIndex == (self.showStartLine - 1):
            # Im in the first rendered line (but NOT  the "0" line) and at the beginning of the line.
            # => move one upward, change showstartLine & cursor placement.
            self.showStartLine -= 1
            self.cursor_Y += self.line_gap

    elif self.chosen_LetterIndex > 0:
        # mid-line or end of the line -> Delete a letter
        self.line_string_list[self.chosen_LineIndex] = self.line_string_list[self.chosen_LineIndex]\
            [:(self.chosen_LetterIndex - 1)] + self.line_string_list[self.chosen_LineIndex][self.chosen_LetterIndex:]

        self.cursor_X -= self.letter_size_X
        self.chosen_LetterIndex -= 1
    else:
        raise ValueError("INVALID CONSTRUCT: handle_keyboard_backspace. \
                         \nLine:" + str(self.chosen_LineIndex) + "\nLetter: " + str(self.chosen_LetterIndex))


def handle_keyboard_delete(self) -> None:

    if self.chosen_LetterIndex < (len(self.line_string_list[self.chosen_LineIndex])):
        # start of the line or mid-line (Cursor stays on point), cut one letter out
        self.line_string_list[self.chosen_LineIndex] = self.line_string_list[self.chosen_LineIndex] \
             [:self.chosen_LetterIndex] + self.line_string_list[self.chosen_LineIndex][(self.chosen_LetterIndex + 1):]

    elif self.chosen_LetterIndex == len(self.line_string_list[self.chosen_LineIndex]):
        # End of a line  (choose next line)
        if self.chosen_LineIndex != (
                self.maxLines - 1):  # NOT in the last line &(prev) at the end of the line, I cannot delete anything
            self.line_string_list[self.chosen_LineIndex] += self.line_string_list[
                self.chosen_LineIndex + 1]  # add the contents of the next line to the current one
            self.line_string_list.pop(
                self.chosen_LineIndex + 1)  # delete the Strings-line in order to move the following lines one upwards
            self.maxLines -= 1  # Keep the variable aligned
            self.rerenderLineNumbers = True
            if self.showStartLine > 0:
                if (self.showStartLine + self.showable_line_numbers_in_editor) > self.maxLines:
                    # The scrollbar is all the way down.
                    # We delete a line, so we have to "pull everything one visual line down"
                    self.showStartLine -= 1  # "pull one visual line down" (array-based)
                    self.cursor_Y += self.line_gap  # move the curser one down.  (visually based)
    else:
        raise ValueError(" INVALID CONSTRUCT: handle_keyboard_delete. \
                         \nLine:" + str(self.chosen_LineIndex) + "\nLetter: " + str(self.chosen_LetterIndex))


def handle_keyboard_arrow_left(self) -> None:
    if self.chosen_LetterIndex > 0:  # mid-line or end of line
        self.chosen_LetterIndex -= 1
        self.cursor_X -= self.letter_size_X
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex == 0:
        # first line, first position, nothing happens
        pass
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:  # Move over into previous Line (if there is any)
        self.chosen_LineIndex -= 1
        self.chosen_LetterIndex = len(self.line_string_list[self.chosen_LineIndex])  # end of previous line
        self.cursor_X = self.xline_start + (len(self.line_string_list[self.chosen_LineIndex]) * self.letter_size_X)
        self.cursor_Y -= self.line_gap
        if self.chosen_LineIndex < self.showStartLine:
            # handling scroll functionality if necessary (moved above shown lines)
            self.showStartLine -= 1
            self.cursor_Y += self.line_gap
            self.rerenderLineNumbers = True


def handle_keyboard_arrow_right(self) -> None:
    if self.chosen_LetterIndex < (len(self.line_string_list[self.chosen_LineIndex])):
        # mid-line or start of the line
        self.chosen_LetterIndex += 1
        self.cursor_X += self.letter_size_X
    elif self.chosen_LetterIndex == len(self.line_string_list[self.chosen_LineIndex]) and \
            not (self.chosen_LineIndex == (self.maxLines - 1)):
        # end of line => move over into the start of the next line

        self.chosen_LetterIndex = 0
        self.chosen_LineIndex += 1
        self.cursor_X = self.xline_start
        self.cursor_Y += self.line_gap
        if self.chosen_LineIndex > (self.showStartLine + self.showable_line_numbers_in_editor - 1):
            # handling scroll functionality if necessary (moved below showed lines)
            self.showStartLine += 1
            self.cursor_Y -= self.line_gap
            self.rerenderLineNumbers = True


def handle_keyboard_arrow_down(self) -> None:
    if self.chosen_LineIndex < (self.maxLines - 1):
        # Not in the last line, downward movement possible
        self.chosen_LineIndex += 1
        self.cursor_Y += self.line_gap

        if len(self.line_string_list[self.chosen_LineIndex]) < self.chosen_LetterIndex:
            # reset letter-index to the end
            self.chosen_LetterIndex = len(self.line_string_list[self.chosen_LineIndex])
            self.cursor_X = (len(self.line_string_list[self.chosen_LineIndex]) * self.letter_size_X) + self.xline_start

        if self.chosen_LineIndex > (self.showStartLine + self.showable_line_numbers_in_editor - 1):
            # handle scrolling functionality if necessary (moved below shown lines)
            self.scrollDown()

    elif self.chosen_LineIndex == (self.maxLines - 1):  # im in the last line and want to jump to its end.
        self.chosen_LetterIndex = len(self.line_string_list[self.chosen_LineIndex])  # end of the line
        self.cursor_X = self.xline_start + (
                len(self.line_string_list[self.chosen_LineIndex]) * self.letter_size_X)


def handle_keyboard_arrow_up(self) -> None:
    if self.chosen_LineIndex == 0:
        # first line, cannot go upwards, so we go to the first position
        self.chosen_LetterIndex = 0
        self.cursor_X = self.xline_start

    elif self.chosen_LineIndex > 0:
        # subsequent lines, upwards movement possible
        self.chosen_LineIndex -= 1
        self.cursor_Y -= self.line_gap

        if len(self.line_string_list[self.chosen_LineIndex]) < self.chosen_LetterIndex:
            # less letters in this line, reset toward the end of the line (to the left)
            self.chosen_LetterIndex = len(self.line_string_list[self.chosen_LineIndex])
            self.cursor_X = (len(self.line_string_list[self.chosen_LineIndex])) * self.letter_size_X + self.xline_start

        if self.chosen_LineIndex < self.showStartLine:  # scroll up one line
            self.scrollUp()


def handle_keyboard_tab(self) -> None:
    for x in range(0, 4):  # insert 4 spaces
        self.handle_keyboard_space()


def handle_keyboard_space(self) -> None:
    # insert 1 space
    self.line_string_list[self.chosen_LineIndex] = \
        self.line_string_list[self.chosen_LineIndex][:self.chosen_LetterIndex] + " " + \
        self.line_string_list[self.chosen_LineIndex][self.chosen_LetterIndex:]

    self.cursor_X += self.letter_size_X
    self.chosen_LetterIndex += 1


def handle_keyboard_return(self) -> None:
    # Get "transfer letters" behind cursor up to the end of the line to next line
    # If the cursor is at the end of the line, transferString is an empty String ("")
    transferString = self.line_string_list[self.chosen_LineIndex][self.chosen_LetterIndex:]

    # Remove transfer letters from the current line
    self.line_string_list[self.chosen_LineIndex] = \
        self.line_string_list[self.chosen_LineIndex][:self.chosen_LetterIndex]

    # set logical cursor indizes and add a new line
    self.chosen_LineIndex += 1
    self.chosen_LetterIndex = 0
    self.maxLines += 1
    self.cursor_X = self.xline_start  # reset cursor to start of the line

    # insert empty line
    self.line_string_list.insert(self.chosen_LineIndex, "")  # logical line

    # Edit the new line -> append transfer letters
    self.line_string_list[self.chosen_LineIndex] = self.line_string_list[self.chosen_LineIndex] + transferString
    self.rerenderLineNumbers = True

    # handle scrolling functionality
    if self.chosen_LineIndex > (self.showable_line_numbers_in_editor - 1):  # Last row, visual representation moves down
        self.showStartLine += 1
    else:  # not in last row, put courser one line down without changing the shown line numbers
        self.cursor_Y += self.line_gap


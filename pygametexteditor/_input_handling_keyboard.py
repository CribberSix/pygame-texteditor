import pygame


def handle_keyboard_input(self, pygame_events):
    self.deleteCounter += 1
    self.deleteCounter = self.deleteCounter % 4
    # TODO: find a good option here. If FPS = 60; then we can delete 15 characters each second
    # FPS are set in __init__.py

    # Detect tapping/holding of the "DELETE" and "BACKSPACE" key
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_DELETE] and self.deleteCounter == 0:
        self.handle_keyboard_delete()
    if pressed_keys[pygame.K_BACKSPACE] and self.deleteCounter == 0:
        self.handle_keyboard_backspace()

    # ___ OTHER KEYS ___ #
    for event in pygame_events:
        if event.type == pygame.QUIT:
            pygame.quit()  # Fixes the bug that pygame takes up space in the RAM when game is just closed by sys.exit()
            exit()
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
                                     pygame.K_BACKSPACE]:  # we handled those separately
                    raise ValueError("No key implementation: " + str(pygame.key.name(event.key)))


def handle_keyboard_backspace(self):

    self.chosen_LetterIndex = int(self.chosen_LetterIndex)  # TODO: Why would it not be of type integer?
    # TODO: Deletion-speed is a bit off
    # TODO: Differentiate between a one-time-press and a longer pressing
    # --> wait x amount of time before deleting the second character if the is being pressed.
    # --> I already do that (self.deleteCounter), but how can I improve it?

    if self.chosen_LetterIndex == 0 and self.chosen_LineIndex == 0:
        # First position and in the first Line -> nothing happens
        pass
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:
        # One Line back if at X-Position 0 and not in the first Line

        # set letter and line index to newly current line
        self.chosen_LineIndex -= 1
        self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
        # set visual cursor one line above and at the end of the line
        self.cursor_Y -= self.line_gap
        self.cursor_X = self.xline_start + (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)

        # take the rest of the former line into the current line
        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] + \
            self.line_String_array[self.chosen_LineIndex + 1]

        # delete the former line
        # LOGICAL lines
        self.line_String_array.pop(self.chosen_LineIndex + 1)
        self.maxLines -= 1
        # VISUAL lines
        self.line_Text_array.pop(self.chosen_LineIndex + 1)
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
        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex]\
            [:(self.chosen_LetterIndex - 1)] + self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]

        self.cursor_X -= self.letter_size_X
        self.chosen_LetterIndex -= 1
    else:
        raise ValueError("INVALID CONSTRUCT: handle_keyboard_backspace. \
                         \nLine:" + str(self.chosen_LineIndex) + "\nLetter: " + str(self.chosen_LetterIndex))


def handle_keyboard_delete(self):

    if self.chosen_LetterIndex < (len(self.line_String_array[self.chosen_LineIndex])):
        # start of the line or mid-line (Cursor stays on point), cut one letter out
        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] \
             [:self.chosen_LetterIndex] + self.line_String_array[self.chosen_LineIndex][(self.chosen_LetterIndex + 1):]

    elif self.chosen_LetterIndex == len(self.line_String_array[self.chosen_LineIndex]):
        # End of a line  (choose next line)
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
                if (self.showStartLine + self.showable_line_numbers_in_editor) > self.maxLines:
                    # The scrollbar is all the way down.
                    # We delete a line, so we have to "pull everything one visual line down"
                    self.showStartLine -= 1  # "pull one visual line down" (array-based)
                    self.cursor_Y += self.line_gap  # move the curser one down.  (visually based)
    else:
        raise ValueError(" INVALID CONSTRUCT: handle_keyboard_delete. \
                         \nLine:" + str(self.chosen_LineIndex) + "\nLetter: " + str(self.chosen_LetterIndex))


def handle_keyboard_arrow_left(self):
    if self.chosen_LetterIndex > 0:  # mid-line or end of line
        self.chosen_LetterIndex -= 1
        self.cursor_X -= self.letter_size_X
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex == 0:
        # first line, first position, nothing happens
        pass
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:  # Move over into previous Line (if there is any)
        self.chosen_LineIndex -= 1
        self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])  # end of previous line
        self.cursor_X = self.xline_start + (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)
        self.cursor_Y -= self.line_gap
        if self.chosen_LineIndex < self.showStartLine:
            # handling scroll functionality if necessary (moved above shown lines)
            self.showStartLine -= 1
            self.cursor_Y += self.line_gap
            self.rerenderLineNumbers = True


def handle_keyboard_arrow_right(self):
    if self.chosen_LetterIndex < (len(self.line_String_array[self.chosen_LineIndex])):
        # mid-line or start of the line
        self.chosen_LetterIndex += 1
        self.cursor_X += self.letter_size_X
    elif self.chosen_LetterIndex == len(self.line_String_array[self.chosen_LineIndex]) and \
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

def handle_keyboard_arrow_down(self):
    if self.chosen_LineIndex < (self.maxLines - 1):
        # Not in the last line, downward movement possible
        self.chosen_LineIndex += 1
        self.cursor_Y += self.line_gap

        if len(self.line_String_array[self.chosen_LineIndex]) < self.chosen_LetterIndex:
            # reset letter-index
            self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
            self.cursor_X = (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X) + self.xline_start

        if self.chosen_LineIndex > (self.showStartLine + self.showable_line_numbers_in_editor - 1):
            # handle scrolling functionality if necessary (moved below shown lines)
            self.showStartLine += 1
            self.cursor_Y -= self.line_gap
            self.rerenderLineNumbers = True
    if self.chosen_LineIndex == (self.maxLines - 1):  # im in the last line and want to jump to its end.
        self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])  # end of the line
        self.cursor_X = self.xline_start + (
                len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)


def handle_keyboard_arrow_up(self):
    if self.chosen_LineIndex == 0:
        # first line, cannot go upwards
        pass
    elif self.chosen_LineIndex > 0:
        # subsequent lines, upwards movement possible
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


def handle_keyboard_tab(self):
    for x in range(0, 4):  # insert 4 spaces
        self.handle_keyboard_space()


def handle_keyboard_space(self):
    # insert 1 space
    self.line_String_array[self.chosen_LineIndex] = \
        self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex] + " " + \
        self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]

    self.cursor_X += self.letter_size_X
    self.chosen_LetterIndex += 1


def handle_keyboard_return(self):
    # Get "transfer letters" behind cursor up to the end of the line to next line
    # If the cursor is at the end of the line, transferString is an empty String ("")
    transferString = self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]

    # Remove transfer letters from the current line
    self.line_String_array[self.chosen_LineIndex] = \
        self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex]
    # re-render current line
    self.line_Text_array[self.chosen_LineIndex] = self.courier_font.render(
        self.line_String_array[self.chosen_LineIndex], 1, self.textColor)

    # set logical cursor indizes and add a new line
    self.chosen_LineIndex += 1
    self.chosen_LetterIndex = 0
    self.maxLines += 1
    self.cursor_X = self.xline_start  # reset cursor to start of the line

    # insert empty line
    self.line_String_array.insert(self.chosen_LineIndex, "")  # logical line
    self.line_Text_array.insert(self.chosen_LineIndex, self.courier_font.render("", 1, (10, 10, 10)))  # visual line

    # Edit the new line -> append transfer letters
    self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] + transferString
    self.rerenderLineNumbers = True

    # handle scrolling functionality
    if self.chosen_LineIndex > (self.showable_line_numbers_in_editor - 1):  # Last row, visual representation moves down
        self.showStartLine += 1
    else:  # not in last row, put courser one line down without changing the shown line numbers
        self.cursor_Y += self.line_gap

import pygame


def reset_after_highlight(self):
    self.dragged_active = False  # deactivate highlight
    self.dragged_finished = True  # highlight is finished

    self.update_caret_position()  # update caret position to chosen_Index (Line+Letter)
    self.last_clickdown_cycle = 0  # reset drag-cycle
    self.last_clickup_cycle = -1


def handle_input_with_highlight(self, input_key):
    # for readability & maintainability we use shorter variable names
    line_start = self.drag_chosen_LineIndex_start
    line_end = self.drag_chosen_LineIndex_end
    letter_start = self.drag_chosen_LetterIndex_start
    letter_end = self.drag_chosen_LetterIndex_end

    if self.dragged_finished and self.dragged_active:
        if input_key in (pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT):
            if input_key == pygame.K_DOWN:
                pass  # we jump one line down from drag_end (if a line exists above, otherwise to the start of the line)
            elif input_key == pygame.K_UP:
                pass  # we jump one line up from drag_end (if a line exists below, otherwise to the end of the line)
            elif input_key == pygame.K_RIGHT:
                if line_start <= line_end:
                    # downward highlight or the same line
                    self.chosen_LineIndex = line_end
                    self.chosen_LetterIndex = letter_end
                else:  # upward highlight
                    self.chosen_LineIndex = line_start
                    self.chosen_LetterIndex = letter_start
            elif input_key == pygame.K_LEFT:
                if line_start <= line_end:
                    # downward highlight or the same line
                    self.chosen_LineIndex = line_start
                    self.chosen_LetterIndex = letter_start
                else:  # upward highlight
                    self.chosen_LineIndex = line_end
                    self.chosen_LetterIndex = letter_end

            self.reset_after_highlight()

        elif input_key in (pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_CAPSLOCK):
            pass  # nothing happens (?)
        # Are there other keys which we have to take into account?

        else:  # normal key -> delete highlighted area and insert key
            if line_start == line_end:  # delete in single line (no line-rearranging)
                self.delete_letter_to_letter(line_start, letter_start, letter_end)
            else:  # multi-line delete
                step = 1 if line_start < line_end else -1
                for i, line_number in enumerate(range(line_start, line_end + step, step)):
                    print("Current: " + str(line_number) + " of: " + str(line_start) + "->" + str(line_end))
                    if i == 0:  # first line
                        if step > 0:  # downward highlighted
                            self.delete_letter_to_end(line_start, letter_start)  # delete right side from start
                        else:
                            self.delete_start_to_letter(line_start, letter_start)  # delete left side from start
                    elif i < len(range(line_start, line_end, 1)):  # middle line
                        # TODO: WATCH OUT FOR NEW INDIZES AFTER DELETION (!)
                        self.delete_entire_line(line_start + 1)  # doesn't it always stay at line_start +1?
                    else:  # last line
                        if step > 0:
                            self.delete_start_to_letter(line_start + 1, letter_end)  # delete left side
                        else:
                            self.delete_letter_to_end(line_start + 1, letter_end)  # delete right side

                # join rest of start/end lines into new line
                l1 = self.line_String_array[line_start]
                l2 = self.line_String_array[line_start + 1]  # which was formerly line_end
                self.line_String_array[line_start] = l1 + l2
                self.delete_entire_line(line_start + 1)  # after copying contents, we need to delete

                # set caret and rerender line_numbers
                self.chosen_LineIndex = line_start if line_start < line_end else line_end
                self.chosen_LetterIndex = letter_start if line_start < line_end else letter_end
                self.rerenderLineNumbers = True
                self.reset_after_highlight()
                self.deleteCounter = 1  # TODO: BUG -> another character gets deleted by mistake


def handle_keyboard_input(self, pygame_events):
    self.deleteCounter += 1
    self.deleteCounter = self.deleteCounter % 4  # If FPS = 60; then we can delete 15 characters each second

    # Detect tapping/holding of the "DELETE" and "BACKSPACE" key
    pressed_keys = pygame.key.get_pressed()
    if self.dragged_finished and self.dragged_active and \
            (pressed_keys[pygame.K_DELETE] or pressed_keys[pygame.K_BACKSPACE]):
        self.handle_input_with_highlight(pygame.K_DELETE)  # delete and backspacke have the same functionality

    elif pressed_keys[pygame.K_DELETE] and self.deleteCounter == 0:
        self.handle_keyboard_delete()  # handle input
        self.reset_text_area_to_caret()  # reset caret if necessary
    elif pressed_keys[pygame.K_BACKSPACE] and self.deleteCounter == 0:
        self.handle_keyboard_backspace()  # handle input
        self.reset_text_area_to_caret()  # reset caret if necessary

    # ___ OTHER KEYS ___ #
    for event in pygame_events:
        if event.type == pygame.KEYDOWN:
            if self.dragged_finished and self.dragged_active:
                self.handle_input_with_highlight(event.key)
            else:
                self.reset_text_area_to_caret()  # reset visual area to include line of caret if necessaryss

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
                                         pygame.K_BACKSPACE, pygame.K_CAPSLOCK]:
                        # we handled the separately, Capslock is apparently implicitly handled when using it

                        # disabled for smooth development:
                        # raise ValueError("No key implementation: " + str(pygame.key.name(event.key)))
                        print("No key implementation: " + str(pygame.key.name(event.key)))


def handle_keyboard_backspace(self):
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

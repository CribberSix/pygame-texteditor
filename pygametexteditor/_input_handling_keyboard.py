
def handle_keyboard_backspace(self):
    self.chosen_LetterIndex = int(self.chosen_LetterIndex)  # TODO: Why would it not be of type integer?
    # TODO: DELETES ALL ROWS BEFORE THE CURSOR (!) --> MOUSE DRAG sideffect?

    if self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:
        # One Line back if at X-Position 0 and not in the first Line
        # Line & Letter Handling
        self.chosen_LineIndex -= 1
        self.cursor_Y -= self.line_gap
        self.cursor_X = self.xline_start + (len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)
        self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])

        # take the rest of the line into the previous line
        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] + \
            self.line_String_array[self.chosen_LineIndex + 1]

        # delete the Strings-line in order to move the following lines one upwards
        self.line_String_array.pop(self.chosen_LineIndex + 1)
        self.maxLines -= 1  # Keep the variable aligned
        self.line_Text_array.pop(
            self.chosen_LineIndex + 1)  # delete the Text-line in order to move the following lines one upwards
        self.rerenderLineNumbers = True

        # Scroll Handling
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
        # mid-line -> Delete a letter (but only if there are letters left) (Cursor moves)
        self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex][
                                                        :(self.chosen_LetterIndex - 1)] + self.line_String_array[
                                                                                              self.chosen_LineIndex][
                                                                                          (
                                                                                              self.chosen_LetterIndex):]
        self.cursor_X -= self.letter_size_X
        self.chosen_LetterIndex -= 1
    # TODO: end of line?


def handle_keyboard_delete(self):
    if self.chosen_LetterIndex < (len(self.line_String_array[self.chosen_LineIndex])):
        # mid-line (Cursor stays on point), cut one letter out
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
        raise ValueError(" INVALID CONSTRUCT: handle_keyboard_delete")


def handle_keyboard_arrow_left(self):
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

def handle_keyboard_arrow_right(self):
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

def handle_keyboard_arrow_down(self):
    if self.chosen_LineIndex < (self.maxLines - 1):  # Not in the last line, i can move downward.
        self.chosen_LineIndex += 1
        self.cursor_Y += self.line_gap
        if len(self.line_String_array[self.chosen_LineIndex]) < self.chosen_LetterIndex:
            self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])
            self.cursor_X = ((len(
                self.line_String_array[self.chosen_LineIndex])) * self.letter_size_X) + self.xline_start
        if self.chosen_LineIndex > (self.showStartLine + self.showable_line_numbers_in_editor - 1):
            # I move downward outside of the rendered lines => "pull the lines up"
            self.showStartLine += 1
            self.cursor_Y -= self.line_gap
            self.rerenderLineNumbers = True
    if self.chosen_LineIndex == (self.maxLines - 1):  # im in the last line and want to jump to its end.
        self.chosen_LetterIndex = len(self.line_String_array[self.chosen_LineIndex])  # end of the line
        self.cursor_X = self.xline_start + (
                len(self.line_String_array[self.chosen_LineIndex]) * self.letter_size_X)


def handle_keyboard_arrow_up(self):
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
    self.line_String_array[self.chosen_LineIndex] = \
        self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex] + "    " + \
        self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]

    self.cursor_X += self.letter_size_X * 4
    self.chosen_LetterIndex += 4


def handle_keyboard_space(self):
    self.line_String_array[self.chosen_LineIndex] = \
        self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex] + " " + \
        self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]

    self.cursor_X += self.letter_size_X
    self.chosen_LetterIndex += 1


def handle_keyboard_return(self):
    transferString = self.line_String_array[self.chosen_LineIndex][self.chosen_LetterIndex:]
    # Transfer letters behind cursor to next line

    # Edit previous line
    self.line_String_array[self.chosen_LineIndex] = \
        self.line_String_array[self.chosen_LineIndex][:self.chosen_LetterIndex]

    self.line_Text_array[self.chosen_LineIndex] = self.Courier_Text_15.render(
        self.line_String_array[self.chosen_LineIndex], 1, self.textColor)  # formatting the line
    self.chosen_LineIndex += 1
    self.chosen_LetterIndex = 0
    self.maxLines += 1
    self.cursor_X = self.xline_start
    self.line_String_array.insert(self.chosen_LineIndex, "")
    self.line_Text_array.insert(self.chosen_LineIndex, self.Courier_Text_15.render("", 1, (10, 10, 10)))

    # EDIT new line with transfer letters
    self.line_String_array[self.chosen_LineIndex] = self.line_String_array[self.chosen_LineIndex] + transferString
    self.rerenderLineNumbers = True

    if self.chosen_LineIndex > (self.showable_line_numbers_in_editor - 1):  # Last row
        self.showStartLine += 1
    else:
        self.cursor_Y += self.line_gap  # not in last row, put courser one line down.

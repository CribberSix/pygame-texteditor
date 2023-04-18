import warnings

import pygame


def handle_keyboard_input(self, pygame_events, pressed_keys) -> None:

    for event in pygame_events:
        if event.type == pygame.KEYDOWN:

            # ___ COMBINATION KEY INPUTS ___
            # Functionality whether something is highlighted or not (highlight all / paste)
            if (
                pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
            ) and event.key == pygame.K_a:
                self.highlight_all()
            elif (
                pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
            ) and event.key == pygame.K_v:
                self.handle_highlight_and_paste()

            # Functionality for when something is highlighted (cut / copy)
            elif self.dragged_finished and self.dragged_active:
                if (
                    pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
                ) and event.key == pygame.K_x:
                    self.handle_highlight_and_cut()
                elif (
                    pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
                ) and event.key == pygame.K_c:
                    self.handle_highlight_and_copy()
                else:
                    self.handle_input_with_highlight(
                        event
                    )  # handle char input on highlight

            # ___ SINGLE KEY INPUTS ___
            else:
                self.reset_text_area_to_caret()  # reset visual area to include line of caret if necessary
                self.chosen_LetterIndex = int(self.chosen_LetterIndex)

                # Detect tapping/holding of the "DELETE" and "BACKSPACE" key while something is highlighted
                if (
                    self.dragged_finished
                    and self.dragged_active
                    and (event.unicode == "\x08" or event.unicode == "\x7f")
                ):
                    # create the uniform event for both keys so we don't have to write two functions
                    deletion_event = pygame.event.Event(
                        pygame.KEYDOWN, key=pygame.K_DELETE
                    )
                    self.handle_input_with_highlight(
                        deletion_event
                    )  # delete and backspace have the same functionality

                # ___ DELETIONS ___
                elif event.unicode == "\x08":  # K_BACKSPACE
                    self.handle_keyboard_backspace()
                    self.reset_text_area_to_caret()  # reset caret if necessary
                elif event.unicode == "\x7f":  # K_DELETE
                    self.handle_keyboard_delete()
                    self.reset_text_area_to_caret()  # reset caret if necessary

                # ___ NORMAL KEYS ___
                # This covers all letters and numbers (not those on numpad).
                elif len(pygame.key.name(event.key)) == 1:
                    self.insert_unicode(event.unicode)

                # ___ NUMPAD KEYS ___
                # for the numbers, numpad must be activated (mod = 4096)
                elif event.mod == 4096 and 1073741913 <= event.key <= 1073741922:
                    self.insert_unicode(event.unicode)
                # all other numpad keys can be triggered with & without mod
                elif event.key in [
                    pygame.K_KP_PERIOD,
                    pygame.K_KP_DIVIDE,
                    pygame.K_KP_MULTIPLY,
                    pygame.K_KP_MINUS,
                    pygame.K_KP_PLUS,
                    pygame.K_KP_EQUALS,
                ]:
                    self.insert_unicode(event.unicode)

                # ___ SPECIAL KEYS ___
                elif event.key == pygame.K_TAB:  # TABULATOR
                    self.handle_keyboard_tab()
                elif event.key == pygame.K_SPACE:  # SPACEBAR
                    self.handle_keyboard_space()
                elif (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER
                ):  # RETURN
                    self.handle_keyboard_return()
                elif event.key == pygame.K_UP:  # ARROW_UP
                    self.handle_keyboard_arrow_up()
                elif event.key == pygame.K_DOWN:  # ARROW_DOWN
                    self.handle_keyboard_arrow_down()
                elif event.key == pygame.K_RIGHT:  # ARROW_RIGHT
                    self.handle_keyboard_arrow_right()
                elif event.key == pygame.K_LEFT:  # ARROW_LEFT
                    self.handle_keyboard_arrow_left()

                else:
                    if event.key not in [
                        pygame.K_RSHIFT,
                        pygame.K_LSHIFT,
                        pygame.K_DELETE,
                        pygame.K_BACKSPACE,
                        pygame.K_CAPSLOCK,
                        pygame.K_LCTRL,
                        pygame.K_RCTRL,
                    ]:
                        # We handled the keys separately
                        # Capslock is apparently implicitly handled when using it in combination
                        warnings.warn(
                            "No implementation for key: "
                            + str(pygame.key.name(event.key)),
                            Warning,
                        )


def insert_unicode(self, unicode) -> None:
    self.editor_lines[self.chosen_LineIndex] = (
        self.editor_lines[self.chosen_LineIndex][: self.chosen_LetterIndex]
        + unicode
        + self.editor_lines[self.chosen_LineIndex][self.chosen_LetterIndex :]
    )
    self.caret_x += self.letter_size_x
    self.chosen_LetterIndex += 1


def handle_keyboard_backspace(self) -> None:
    if self.chosen_LetterIndex == 0 and self.chosen_LineIndex == 0:
        # First position and in the first Line -> nothing happens
        pass
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0:
        # One Line back if at X-Position 0 and not in the first Line

        # set letter and line index to newly current line
        self.chosen_LineIndex -= 1
        self.chosen_LetterIndex = len(self.editor_lines[self.chosen_LineIndex])
        # set visual cursor one line above and at the end of the line
        self.caret_y -= self.line_height_including_gap
        self.caret_x = self.xline_start + (
            len(self.editor_lines[self.chosen_LineIndex]) * self.letter_size_x
        )

        # take the rest of the former line into the current line
        self.editor_lines[self.chosen_LineIndex] = (
            self.editor_lines[self.chosen_LineIndex]
            + self.editor_lines[self.chosen_LineIndex + 1]
        )

        # delete the former line
        # LOGICAL lines
        self.editor_lines.pop(self.chosen_LineIndex + 1)
        # VISUAL lines
        self.rerender_line_numbers = True

        # Handling of the resulting scrolling functionality of removing one line
        if self.first_showable_line_index > 0:
            if (
                self.first_showable_line_index + self.showable_line_numbers_in_editor
            ) > len(self.editor_lines):
                # The scrollbar is all the way down. We delete a line,
                # so we have to "pull everything one visual line down"
                self.first_showable_line_index -= (
                    1  # "pull one visual line down" (array-based)
                )
                self.caret_y += (
                    self.line_height_including_gap
                )  # move the curser one down.  (visually based)
        if self.chosen_LineIndex == (self.first_showable_line_index - 1):
            # Im in the first rendered line (but NOT  the "0" line) and at the beginning of the line.
            # => move one upward, change showstartLine & cursor placement.
            self.first_showable_line_index -= 1
            self.caret_y += self.line_height_including_gap

    elif self.chosen_LetterIndex > 0:
        # mid-line or end of the line -> Delete a letter
        self.editor_lines[self.chosen_LineIndex] = (
            self.editor_lines[self.chosen_LineIndex][: (self.chosen_LetterIndex - 1)]
            + self.editor_lines[self.chosen_LineIndex][self.chosen_LetterIndex :]
        )

        self.caret_x -= self.letter_size_x
        self.chosen_LetterIndex -= 1
    else:
        raise ValueError(
            "INVALID CONSTRUCT: handle_keyboard_backspace. \
                         \nLine:"
            + str(self.chosen_LineIndex)
            + "\nLetter: "
            + str(self.chosen_LetterIndex)
        )


def handle_keyboard_delete(self) -> None:

    if self.chosen_LetterIndex < (len(self.editor_lines[self.chosen_LineIndex])):
        # start of the line or mid-line (Cursor stays on point), cut one letter out
        self.editor_lines[self.chosen_LineIndex] = (
            self.editor_lines[self.chosen_LineIndex][: self.chosen_LetterIndex]
            + self.editor_lines[self.chosen_LineIndex][(self.chosen_LetterIndex + 1) :]
        )

    elif self.chosen_LetterIndex == len(self.editor_lines[self.chosen_LineIndex]):
        # End of a line  (choose next line)
        if self.chosen_LineIndex != (
            len(self.editor_lines) - 1
        ):  # NOT in the last line &(prev) at the end of the line, I cannot delete anything
            self.editor_lines[self.chosen_LineIndex] += self.editor_lines[
                self.chosen_LineIndex + 1
            ]  # add the contents of the next line to the current one
            self.editor_lines.pop(
                self.chosen_LineIndex + 1
            )  # delete the Strings-line in order to move the following lines one upwards
            self.rerender_line_numbers = True
            if self.first_showable_line_index > 0:
                if (
                    self.first_showable_line_index
                    + self.showable_line_numbers_in_editor
                ) > len(self.editor_lines):
                    # The scrollbar is all the way down.
                    # We delete a line, so we have to "pull everything one visual line down"
                    self.first_showable_line_index -= (
                        1  # "pull one visual line down" (array-based)
                    )
                    self.caret_y += (
                        self.line_height_including_gap
                    )  # move the curser one down.  (visually based)
    else:
        raise ValueError(
            " INVALID CONSTRUCT: handle_keyboard_delete. \
                         \nLine:"
            + str(self.chosen_LineIndex)
            + "\nLetter: "
            + str(self.chosen_LetterIndex)
        )


def handle_keyboard_arrow_left(self) -> None:
    if self.chosen_LetterIndex > 0:  # mid-line or end of line
        self.chosen_LetterIndex -= 1
        self.caret_x -= self.letter_size_x
    elif self.chosen_LetterIndex == 0 and self.chosen_LineIndex == 0:
        # first line, first position, nothing happens
        pass
    elif (
        self.chosen_LetterIndex == 0 and self.chosen_LineIndex > 0
    ):  # Move over into previous Line (if there is any)
        self.chosen_LineIndex -= 1
        self.chosen_LetterIndex = len(
            self.editor_lines[self.chosen_LineIndex]
        )  # end of previous line
        self.caret_x = self.xline_start + (
            len(self.editor_lines[self.chosen_LineIndex]) * self.letter_size_x
        )
        self.caret_y -= self.line_height_including_gap
        if self.chosen_LineIndex < self.first_showable_line_index:
            # handling scroll functionality if necessary (moved above shown lines)
            self.first_showable_line_index -= 1
            self.caret_y += self.line_height_including_gap
            self.rerender_line_numbers = True


def handle_keyboard_arrow_right(self) -> None:
    if self.chosen_LetterIndex < (len(self.editor_lines[self.chosen_LineIndex])):
        # mid-line or start of the line
        self.chosen_LetterIndex += 1
        self.caret_x += self.letter_size_x
    elif self.chosen_LetterIndex == len(
        self.editor_lines[self.chosen_LineIndex]
    ) and not (self.chosen_LineIndex == (len(self.editor_lines) - 1)):
        # end of line => move over into the start of the next line

        self.chosen_LetterIndex = 0
        self.chosen_LineIndex += 1
        self.caret_x = self.xline_start
        self.caret_y += self.line_height_including_gap
        if self.chosen_LineIndex > (
            self.first_showable_line_index + self.showable_line_numbers_in_editor - 1
        ):
            # handling scroll functionality if necessary (moved below showed lines)
            self.first_showable_line_index += 1
            self.caret_y -= self.line_height_including_gap
            self.rerender_line_numbers = True


def handle_keyboard_arrow_down(self) -> None:
    if self.chosen_LineIndex < (len(self.editor_lines) - 1):
        # Not in the last line, downward movement possible
        self.chosen_LineIndex += 1
        self.caret_y += self.line_height_including_gap

        if len(self.editor_lines[self.chosen_LineIndex]) < self.chosen_LetterIndex:
            # reset letter-index to the end
            self.chosen_LetterIndex = len(self.editor_lines[self.chosen_LineIndex])
            self.caret_x = (
                len(self.editor_lines[self.chosen_LineIndex]) * self.letter_size_x
            ) + self.xline_start

        if self.chosen_LineIndex > (
            self.first_showable_line_index + self.showable_line_numbers_in_editor - 1
        ):
            # handle scrolling functionality if necessary (moved below shown lines)
            self.scrollDown()

    elif self.chosen_LineIndex == (len(self.editor_lines) - 1):
        # In the last line and want to jump to its end.
        self.chosen_LetterIndex = len(
            self.editor_lines[self.chosen_LineIndex]
        )  # end of the line
        self.caret_x = self.xline_start + (
            len(self.editor_lines[self.chosen_LineIndex]) * self.letter_size_x
        )


def handle_keyboard_arrow_up(self) -> None:
    if self.chosen_LineIndex == 0:
        # first line, cannot go upwards, so we go to the first position
        self.chosen_LetterIndex = 0
        self.caret_x = self.xline_start

    elif self.chosen_LineIndex > 0:
        # subsequent lines, upwards movement possible
        self.chosen_LineIndex -= 1
        self.caret_y -= self.line_height_including_gap

        if len(self.editor_lines[self.chosen_LineIndex]) < self.chosen_LetterIndex:
            # less letters in this line, reset toward the end of the line (to the left)
            self.chosen_LetterIndex = len(self.editor_lines[self.chosen_LineIndex])
            self.caret_x = (
                len(self.editor_lines[self.chosen_LineIndex])
            ) * self.letter_size_x + self.xline_start

        if self.chosen_LineIndex < self.first_showable_line_index:  # scroll up one line
            self.scrollUp()


def handle_keyboard_tab(self) -> None:
    for x in range(0, 4):  # insert 4 spaces
        self.handle_keyboard_space()


def handle_keyboard_space(self) -> None:
    # insert 1 space
    self.editor_lines[self.chosen_LineIndex] = (
        self.editor_lines[self.chosen_LineIndex][: self.chosen_LetterIndex]
        + " "
        + self.editor_lines[self.chosen_LineIndex][self.chosen_LetterIndex :]
    )

    self.caret_x += self.letter_size_x
    self.chosen_LetterIndex += 1


def handle_keyboard_return(self) -> None:
    # Get "transfer letters" behind cursor up to the end of the line to next line
    # If the cursor is at the end of the line, transferString is an empty String ("")
    transferString = self.editor_lines[self.chosen_LineIndex][self.chosen_LetterIndex :]

    # Remove transfer letters from the current line
    self.editor_lines[self.chosen_LineIndex] = self.editor_lines[self.chosen_LineIndex][
        : self.chosen_LetterIndex
    ]

    # set logical cursor indizes and add a new line
    self.chosen_LineIndex += 1
    self.chosen_LetterIndex = 0
    self.caret_x = (
        self.xline_start + 1
    )  # reset cursor to start of the line, plus 1 pixel to be visible.

    # insert empty line
    self.editor_lines.insert(self.chosen_LineIndex, "")  # logical line

    # Edit the new line -> append transfer letters
    self.editor_lines[self.chosen_LineIndex] = (
        self.editor_lines[self.chosen_LineIndex] + transferString
    )
    self.rerender_line_numbers = True

    # handle scrolling functionality
    if self.chosen_LineIndex > (
        self.showable_line_numbers_in_editor - 1
    ):  # Last row, visual representation moves down
        self.first_showable_line_index += 1
    else:  # not in last row, put courser one line down without changing the shown line numbers
        self.caret_y += self.line_height_including_gap

import pygame
import pyperclip


def handle_input_with_highlight(self, input_event) -> None:
    """
    Handles key-downs after a drag operation was finished and the highlighted area (drag) is still active.
    For arrow keys we merely jump to the destination.
    For other character-keys we remove the highlighted area and replace it (also over multiple lines)
    with the chosen letter.
    """
    # for readability & maintainability we use shorter variable names
    line_start = self.drag_chosen_LineIndex_start
    line_end = self.drag_chosen_LineIndex_end
    letter_start = self.drag_chosen_LetterIndex_start
    letter_end = self.drag_chosen_LetterIndex_end

    if self.dragged_finished and self.dragged_active:
        if input_event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT):
            # deselect highlight
            if input_event.key == pygame.K_DOWN:
                self.jump_to_end(line_start, line_end, letter_start, letter_end)
            elif input_event.key == pygame.K_UP:
                self.jump_to_start(line_start, line_end, letter_start, letter_end)
            elif input_event.key == pygame.K_RIGHT:
                self.jump_to_end(line_start, line_end, letter_start, letter_end)
            elif input_event.key == pygame.K_LEFT:
                self.jump_to_start(line_start, line_end, letter_start, letter_end)
            self.reset_after_highlight()

        elif input_event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_CAPSLOCK, pygame.K_RCTRL, pygame.K_LCTRL):
            pass  # nothing happens, we wait for the second key with which it is being used in combination

        else:  # other key -> delete highlighted area and insert key (if not esc/delete)
            if line_start == line_end:  # delete in single line
                if letter_start > letter_end:  # swap variables based on left/right highlight to make code more readable
                    letter_start, letter_end = letter_end, letter_start
                self.delete_letter_to_letter(line_start, letter_start, letter_end)

            else:  # multi-line delete
                if line_start > line_end:  # swap variables based on up/downward highlight to make code more readable
                    line_start, line_end = line_end, line_start
                    letter_start, letter_end = letter_end, letter_start

                for i, line_number in enumerate(range(line_start, line_end + 1)):
                    if i == 0:  # first line
                        self.delete_letter_to_end(line_start, letter_start)  # delete right side from start
                    elif i < (line_end - line_start):
                        self.delete_entire_line(line_start + 1)  # stays at line_start +1 as we delete on the fly (!)
                    else:  # last line
                        self.delete_start_to_letter(line_start + 1, letter_end)  # delete left side of new last line

                # join rest of start/end lines into new line in multiline delete
                self.line_string_list[line_start] = self.line_string_list[line_start] + \
                                                     self.line_string_list[line_start + 1]
                self.delete_entire_line(line_start + 1)  # after copying contents, we need to delete the other line

            # set caret and rerender line_numbers
            self.chosen_LineIndex = line_start if line_start <= line_end else line_end  # start for single_line
            self.chosen_LetterIndex = letter_start if line_start <= line_end else letter_end
            self.rerenderLineNumbers = True
            self.reset_after_highlight()

            # insert key unless delete/backspace
            if input_event.key not in (pygame.K_DELETE, pygame.K_BACKSPACE):
                self.insert_unicode(input_event.unicode)


def handle_highlight_and_paste(self):
    """
    Paste clipboard into cursor position.
    Replace highlighted area if highlight, else normal insert.
    """

    # DELETE highlighted section if something is highlighted
    if self.dragged_finished and self.dragged_active:
        delete_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DELETE)  # create artifical delete event
        self.handle_input_with_highlight(delete_event)

    # PASTE from clipboard
    paste_string = pyperclip.paste()
    line_split = paste_string.split("\r\n")  # split into lines
    if len(line_split) == 1:  # no linebreaks
        self.line_string_list[self.chosen_LineIndex] = \
            self.line_string_list[self.chosen_LineIndex][:self.chosen_LetterIndex] \
            + line_split[0] + \
            self.line_string_list[self.chosen_LineIndex][self.chosen_LetterIndex:]

        self.chosen_LetterIndex = self.chosen_LetterIndex + len(line_split[0])

    else:
        rest_of_line = self.line_string_list[self.chosen_LineIndex][self.chosen_LetterIndex:]  # store for later
        for i, line in enumerate(line_split):
            if i == 0:  # first line to insert
                self.line_string_list[self.chosen_LineIndex] = \
                    self.line_string_list[self.chosen_LineIndex][:self.chosen_LetterIndex] + line
            elif i < len(line_split) - 1:  # middle line -> insert new line!
                self.line_string_list[self.chosen_LineIndex + i: self.chosen_LineIndex + i] = [line]
                self.maxLines += 1
            else:  # last line
                self.line_string_list[self.chosen_LineIndex + i: self.chosen_LineIndex + i] = [line + rest_of_line]
                self.maxLines += 1

                self.chosen_LetterIndex = len(line)
                self.chosen_LineIndex = self.chosen_LineIndex + i

    self.update_caret_position()
    self.rerenderLineNumbers = True


def handle_highlight_and_copy(self):
    """
    Copy highlighted String into clipboard if anything is highlighted, else no action.
    """
    copy_string = self.get_highlighted_characters()
    pyperclip.copy(copy_string)


def handle_highlight_and_cut(self):
    """
    Copy highlighted String into clipboard if anything is highlighted, else no action.
    Delete highlighted part of the text.
    """
    # Copy functionality
    copy_string = self.get_highlighted_characters()  # copy characters
    pyperclip.copy(copy_string)

    # Cut / delete functionality
    delete_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DELETE)  # create artifical event
    self.handle_input_with_highlight(delete_event)

    self.update_caret_position()

def highlight_all(self):
    """
    Highlight entire text.
    """
    # set artifical drag and cursor position
    self.set_drag_start_before_first_line()
    self.set_drag_end_after_last_line()
    self.update_caret_position_by_drag_end()
    # activate highlight
    self.dragged_finished = True
    self.dragged_active = True


def get_highlighted_characters(self) -> str:
    """
    Returns the highlighted characters (single- and multiple-line) from the editor (self.line_string_list)
    """
    if self.dragged_finished and self.dragged_active:
        line_start = self.drag_chosen_LineIndex_start
        line_end = self.drag_chosen_LineIndex_end
        letter_start = self.drag_chosen_LetterIndex_start
        letter_end = self.drag_chosen_LetterIndex_end

        if self.drag_chosen_LineIndex_start == self.drag_chosen_LineIndex_end:
            # single-line highlight
            return self.get_line_from_char_to_char(self.drag_chosen_LineIndex_start, self.drag_chosen_LetterIndex_start,
                                                   self.drag_chosen_LetterIndex_end)

        else:  # multi-line highlight
            if line_start > line_end:  # swap variables based on up/downward highlight to make code more readable
                line_start, line_end = line_end, line_start
                letter_start, letter_end = letter_end, letter_start

            # loop through highlighted lines
            copied_chars = ""
            for i, line_index in enumerate(range(line_start, line_end+1)):
                if i == 0:  # first line
                    copied_chars = self.get_line_from_char_to_end(line_index, letter_start)
                elif i < len(range(line_start, line_end)):  # middle line
                    copied_chars = copied_chars + "\r\n" + self.get_entire_line(line_index)
                else:  # last line
                    copied_chars = copied_chars + "\r\n" + self.get_line_from_start_to_char(line_index, letter_end)

            return copied_chars
    else:
        return ""


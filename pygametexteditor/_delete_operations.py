
def delete_letter_to_end(self, line, letter) -> None:
    """
    Deletes within a line from a letter by index to the end of the line.
    """
    self.line_String_array[line] = self.line_String_array[line][:letter]


def delete_start_to_letter(self, line, letter) -> None:
    """
    Deletes within a line from the start of the line to a letter by index..
    """
    self.line_String_array[line] = self.line_String_array[line][letter:]


def delete_letter_to_letter(self, line, letter_start, letter_end) -> None:
    """
    Deletes within a line from a letter to a letter by index..
    """
    self.line_String_array[line] = self.line_String_array[line][:letter_start] + \
            self.line_String_array[line][letter_end:]


def delete_entire_line(self, line) -> None:
    """
    Deletes an entire line
    """
    self.line_String_array.pop(line)
    self.line_Text_array.pop(line)  # also delete surface (!)
    self.maxLines -= 1


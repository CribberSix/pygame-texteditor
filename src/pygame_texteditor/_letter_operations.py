def delete_letter_to_end(self, line, letter) -> None:
    """
    Deletes within a line from a letter by index to the end of the line.
    """
    self.editor_lines[line] = self.editor_lines[line][:letter]


def delete_start_to_letter(self, line, letter) -> None:
    """
    Deletes within a line from the start of the line to a letter by index..
    """
    self.editor_lines[line] = self.editor_lines[line][letter:]


def delete_letter_to_letter(self, line, letter_start, letter_end) -> None:
    """
    Deletes within a line from a letter to a letter by index..
    """
    self.editor_lines[line] = (
        self.editor_lines[line][:letter_start] + self.editor_lines[line][letter_end:]
    )


def delete_entire_line(self, line) -> None:
    """
    Deletes an entire line
    """
    self.editor_lines.pop(line)


def get_entire_line(self, line_index) -> str:
    return self.editor_lines[line_index]


def get_line_from_start_to_char(self, line_index, char_index) -> str:
    return self.editor_lines[line_index][0:char_index]


def get_line_from_char_to_end(self, line_index, char_index) -> str:
    return self.editor_lines[line_index][char_index:]


def get_line_from_char_to_char(self, line_index, char1, char2) -> str:
    if char1 < char2:
        return self.editor_lines[line_index][char1:char2]
    else:
        return self.editor_lines[line_index][char2:char1]

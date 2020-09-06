
def delete_letter_to_end(self, line, letter) -> None:
    """
    Deletes within a line from a letter by index to the end of the line.
    """
    pass


def delete_start_to_letter(self, line, letter) -> None:
    """
    Deletes within a line from the start of the line to a letter by index..
    """
    pass


def delete_entire_line(self, line) -> None:
    """
    Deletes an entire line
    """
    #for x in self.line_String_array:
    #    print(x)
    self.line_String_array.pop(line)
    self.line_Text_array.pop(line)  # also delete surface (!)
    self.maxLines -= 1
    #for x in self.line_String_array:
    #    print(x)


def delete_letter_to_letter(self, line, letter_start, letter_end) -> None:
    """
    Deletes within a line from a letter to a letter by index..
    """
    pass

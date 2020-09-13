
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

#print(find_nth("this 'test' is a 'test' of course 'test'", "'", 10))

def render_line_contents_syntax_coloring(self) -> None:
    """
    Rendering line contests with syntax coloring.
    We create a dict for every part of the line and include which letters are contained, the type and the color.
    So far implemented:
    - comments
    TODO:
    - quoted Strings
    - keywords
    - standalone - numbers
    """

    # Preparation of the rendering:
    self.yline = self.yline_start
    first_line = self.showStartLine
    if self.showable_line_numbers_in_editor < len(self.line_Text_array):
        # we got more text than we are able to display
        last_line = self.showStartLine + self.showable_line_numbers_in_editor
    else:
        last_line = self.maxLines

    # COLOR RENDERING START
    # For now, we recreate all of it every frame (!)
    rendering_list = []
    for line in self.line_Text_array:
        rendering_list.append([])  # create empty list for each line

    for i, line in enumerate(self.line_String_array):

        # SPLIT COMMENTS
        new_line = line.split('#', 1)  # split on first occurence
        rendering_list[i].append({'letters': new_line[0], 'type': 'letters', 'color': self.textColor})
        try:
            rendering_list[i].append(
                {'letters': "#" + new_line[1], 'type': 'comment', 'color': self.textColor_comments})
        except IndexError:
            pass  # no comments found in this line

        # TODO: SPLIT ON QUOTES
        quotes = []
        for i in range(0, 101, 2):  # identify the location of pairs of quotes
            start = find_nth(new_line[0], "'", i)
            end = find_nth(new_line[0], "'", i+1)
            if start == -1:  # no more to be found, stop searching
                break
            quotes.append((start, end))

        for tp in quotes:
            # create surfaces for each
            start = tp[0]
            end = 1000 if tp[1] == -1 else tp[1]  # in case we have no end, rest of string is colored as text.


    # Actual line rendering based on dict-keys
    for line_array in rendering_list[first_line: last_line]:
        xcoord = self.xline_start
        for part in line_array:
            surface = self.courier_font.render(part['letters'], 1, part['color'])
            self.screen.blit(surface, (xcoord, self.yline))

            xcoord = xcoord + (len(part['letters']) * self.letter_size_X)  # next line-part prep
        self.yline += self.line_gap  # next line prep

    # self.textColor = (171, 178, 191)  # (171, 178, 191)

    # self.line_Text_array[self.chosen_LineIndex] = self.courier_font.render(render_string, 1, self.textColor)

    # self.line_Text_array.append(self.courier_font.render(new_line[0], 1, (160, 160, 160)))

    # create a surface based on spacebars
    # new_line = [e+" " for e in line.split(" ") if e]


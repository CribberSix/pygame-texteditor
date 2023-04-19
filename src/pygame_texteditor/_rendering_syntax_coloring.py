from typing import Dict, List


def get_single_color_dicts(self) -> List[List[Dict]]:
    """Convert the editor text into a list of single color tokens which can be used to be rendered.

    Every line is one sublist. Since only one color is applied, an entire line can be a single token.

    :return List[List[Dict]]:
    """
    return [
        [{"chars": line, "type": "normal", "color": self.color_text}]
        for line in self.editor_lines
    ]


def get_syntax_coloring_dicts(self) -> List[List[Dict]]:
    """Convert the editor text into a list of differently colored tokens which can be used to be rendered.

    Every line is one sublist which contains different tokens (dicts) based on its contents.
    We create a dict for every token of every line and include the characters, a pseudo token-type and the color.

    :return List[List[Dict]]: a list containing lines (=a list of tokens (=dicts)).
    """
    return [
        self.color_formatter.format(self.lexer.get_tokens(line))
        for line in self.editor_lines
    ]

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatter import Formatter
from pygments.token import Token, is_token_subtype
from typing import List, Dict


class PybrainzzFormatter:

    def __init__(self):
        self.textColor = (255, 255, 255)  # white
        self.textColor_comments = (119, 115, 115)  # brighter shade of background
        self.textColor_quotes = (231, 219, 116)  # bright yellow
        self.textColor_operators = (249, 36, 114)  # bright red
        self.textColor_keywords = (237, 36, 36)   # bright blue -> def
        self.textColor_function = (166, 226, 43)  # bright green -> function name
        self.textColor_builtin = (104, 216, 239)  # bright blue -> print

    def format(self, tokensource) -> List[Dict]:
        dicts = []
        for ttype, value in tokensource:
            if ttype != Token.Text:
                print(value + " - " + str(ttype))

            # NAME.FUNCTION
            if ttype == Token.Name.Function:
                dicts.append({'chars': value, 'type': 'function', 'color': self.textColor_function})

            # BUILTIN
            elif ttype == Token.Name.Builtin:
                dicts.append({'chars': value, 'type': 'builtin', 'color': self.textColor_builtin})

            # LITERAL.STRING(.*)
            elif ttype == Token.Literal.String.Affix:
                dicts.append({'chars': value, 'type': 'builtin', 'color': self.textColor_builtin})
            elif is_token_subtype(ttype, Token.Literal.String):
                dicts.append({'chars': value, 'type': 'quotes', 'color': self.textColor_quotes})

            # OPERATOR.*
            elif is_token_subtype(ttype, Token.Operator):
                dicts.append({'chars': value, 'type': 'operators', 'color': self.textColor_operators})

            # KEYWORD.*
            elif is_token_subtype(ttype, Token.Keyword):
                dicts.append({'chars': value, 'type': 'keywords', 'color': self.textColor_keywords})

            # COMMENT.*
            elif is_token_subtype(ttype, Token.Comment):
                dicts.append({'chars': value, 'type': 'comments', 'color': self.textColor_comments})

            elif value == '\n':  # since we parse line-by-line, we need to exclude the linebreak character
                pass

            # REST
            else:
                dicts.append({'chars': value, 'type': 'text', 'color': self.textColor})

        return dicts

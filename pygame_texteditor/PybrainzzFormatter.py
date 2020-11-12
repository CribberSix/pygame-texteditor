from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatter import Formatter
from pygments.token import Token, is_token_subtype
from typing import List, Dict, Tuple
import os
import yaml
import re


class PybrainzzFormatter:

    def __init__(self):
        self.textColor_normal = (0, 0, 0)
        self.textColor_comments = (0, 0, 0)
        self.textColor_quotes = (0, 0, 0)
        self.textColor_operators = (0, 0, 0)
        self.textColor_keywords = (0, 0, 0)
        self.textColor_function = (0, 0, 0)
        self.textColor_builtin = (0, 0, 0)

    def format(self, tokensource: List[Tuple]) -> List[Dict]:
        """
        Input is a list of tuples. Each tuple contains the Token and the corresponding characters of said token.
        For different types of tokens the function creates a dict with the three keys:
        - chars -> String
        - type -> String
        - color (rgb color -> (0,0,0) )
        Depending on the type of token a color is assigned.
        """

        dicts = []
        for ttype, value in tokensource:
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
                dicts.append({'chars': value, 'type': 'text', 'color': self.textColor_normal})

        return dicts

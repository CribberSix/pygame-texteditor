from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatter import Formatter
from pygments.token import Token, is_token_subtype
from typing import List, Dict, Tuple
import os
import yaml
import re


class PybrainzzFormatter:

    def __init__(self, style='dark'):
        self.textColor_normal = (0, 0, 0)
        self.textColor_comments = (0, 0, 0)
        self.textColor_quotes = (0, 0, 0)
        self.textColor_operators = (0, 0, 0)
        self.textColor_keywords = (0, 0, 0)
        self.textColor_function = (0, 0, 0)
        self.textColor_builtin = (0, 0, 0)

        self.set_colorscheme(style)

    def set_colorscheme(self, style):
        def get_rgb_by_key(key) -> Tuple:
            pattern = r'(\d{1,3})'
            return tuple([int(x) for x in re.findall(pattern, colors[key])])

        try:
            with open(os.getcwd() + r"\pygametexteditor\elements\colorstyles\\" + style + "-syntax.yml") as file:
                colors = yaml.load(file, Loader=yaml.FullLoader)

                self.textColor_normal = get_rgb_by_key('textColor_normal')
                self.textColor_comments = get_rgb_by_key('textColor_comments')
                self.textColor_quotes = get_rgb_by_key('textColor_quotes')
                self.textColor_operators = get_rgb_by_key('textColor_operators')
                self.textColor_keywords = get_rgb_by_key('textColor_keywords')
                self.textColor_function = get_rgb_by_key('textColor_function')
                self.textColor_builtin = get_rgb_by_key('textColor_builtin')

        except FileNotFoundError:
            raise FileNotFoundError("No file named '" + style +
                                    r"-syntax.yml' found in the searched directory \elements\colorstyles.")
        except KeyError:
            raise KeyError("Not all necessary keys were found in the " + style + "-syntax.yml file.")

    def format(self, tokensource) -> List[Dict]:
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

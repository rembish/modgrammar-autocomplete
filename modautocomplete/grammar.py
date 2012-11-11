from string import ascii_letters, digits

from modgrammar import GrammarClass, Grammar
from modgrammar import Literal as _Literal, WORD as Word
from modgrammar.util import make_classdict, error_result

__all__ = [
    'Grammar', 'Word',
    'Literal', 'CaselessLiteral',
    'Keyword', 'CaselessKeyword',
]

DEFAULT_KEYWORD_CHARACTERS = ascii_letters + digits + '$_'

# Synchonized with pyparsing class definitions.

class _CaselessLiteral(_Literal):
    @classmethod
    def grammar_parse(cls, text, index, sessiondata):
        tstring = text.string.upper()
        while (len(cls.string) + index > len(text.string)) and cls.string.upper().startswith(tstring[index:]):
            if text.eof:
                break
            text = yield (None, None)

        if text.string.upper().startswith(cls.string.upper(), index):
            yield (len(cls.string), cls(cls.string))
        yield error_result(index, cls)

class _Keyword(_Literal):
    grammar_hashattrs = ('string', 'keyword_chars')

    @classmethod
    def grammar_parse(cls, text, index, sessiondata):
        while (len(cls.string) + index > len(text.string)) and cls.string.startswith(text.string[index:]):
            if text.eof:
                break
            text = yield (None, None)

        try:
            next_char = text.string[index + len(cls.string)]
        except IndexError:
            next_char = None

        if text.string.startswith(cls.string, index) and (not next_char or next_char not in cls.keyword_chars):
            yield (len(cls.string), cls(cls.string))
        yield error_result(index, cls)

class _CaselessKeyword(_Keyword):
    @classmethod
    def grammar_parse(cls, text, index, sessiondata):
        tstring = text.string.upper()
        while (len(cls.string) + index > len(text.string)) and cls.string.upper().startswith(tstring[index:]):
            if text.eof:
                break
            text = yield (None, None)

        try:
            next_char = text.string[index + len(cls.string)]
        except IndexError:
            next_char = None

        if text.string.upper().startswith(cls.string.upper(), index) and (not next_char or next_char not in cls.keyword_chars):
            yield (len(cls.string), cls(cls.string))
        yield error_result(index, cls)

def Literal(string, **kwargs):
    kwargs['grammar_name'] = kwargs.get('grammar_name', "Literal({0!r})".format(string))
    cdict = make_classdict(_Literal, (), kwargs, string=string)
    return GrammarClass("<Literal>", (_Literal, ), cdict)

def CaselessLiteral(string, **kwargs):
    kwargs['grammar_name'] = kwargs.get('grammar_name', "CaselessLiteral({0!r})".format(string))
    cdict = make_classdict(_CaselessLiteral, (), kwargs, string=string)
    return GrammarClass("<CaselessLiteral>", (_CaselessLiteral, ), cdict)

def Keyword(string, keyword_chars=DEFAULT_KEYWORD_CHARACTERS, **kwargs):
    kwargs['grammar_name'] = kwargs.get('grammar_name', "Keyword({0!r})".format(string))
    cdict = make_classdict(_Keyword, (), kwargs, string=string, keyword_chars=keyword_chars)
    return GrammarClass("<Keyword>", (_Keyword, ), cdict)

def CaselessKeyword(string, keyword_chars=DEFAULT_KEYWORD_CHARACTERS, **kwargs):
    kwargs['grammar_name'] = kwargs.get('grammar_name', "CaselessKeyword({0!r})".format(string))
    cdict = make_classdict(_CaselessKeyword, (), kwargs, string=string, keyword_chars=keyword_chars)
    return GrammarClass("<Keyword>", (_CaselessKeyword, ), cdict)

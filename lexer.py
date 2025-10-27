from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TokenKind(Enum):

    KW_I32 = auto()
    KW_I64 = auto()
    KW_BOOL = auto()
    KW_MUT = auto()
    KW_RETURN = auto()
    KW_IF = auto()
    KW_ELSE = auto()

    
    TRUE = auto()
    FALSE = auto()
    ID = auto()
    NUMBER = auto()


    LBRACE = auto()
    RBRACE = auto()
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    EQEQ = auto()
    NOTEQ = auto()
    NOT = auto()

    EOF = auto()


@dataclass
class Token:
    kind: TokenKind
    text: str

    def __repr__(self):
        return f"Token({self.kind.name}, '{self.text}')"


def simple_lexer(source_tokens: List[str]) -> List['Token']:
    """
    Extremely simple lexer that expects a pre-tokenized list of lexemes.
    Suitable for our educational compiler pipeline.
    """
    mapping = {
       
        "i32": TokenKind.KW_I32,
        "i64": TokenKind.KW_I64,
        "bool": TokenKind.KW_BOOL,
        "mut": TokenKind.KW_MUT,
        "return": TokenKind.KW_RETURN,
        "if": TokenKind.KW_IF,
        "else": TokenKind.KW_ELSE,
        # bool literals
        "true": TokenKind.TRUE,
        "false": TokenKind.FALSE,
        # symbols
        "{": TokenKind.LBRACE,
        "}": TokenKind.RBRACE,
        "=": TokenKind.ASSIGN,
        "+": TokenKind.PLUS,
        "-": TokenKind.MINUS,
        "*": TokenKind.MUL,
        "==": TokenKind.EQEQ,
        "!=": TokenKind.NOTEQ,
        "!": TokenKind.NOT,
    }

    tokens: List[Token] = []
    for s in source_tokens:
        if s in mapping:
            tokens.append(Token(mapping[s], s))
        elif s.isidentifier():
            tokens.append(Token(TokenKind.ID, s))
        else:
       
            try:
                int(s)
                tokens.append(Token(TokenKind.NUMBER, s))
            except ValueError:
                raise ValueError(f"Unknown token: {s}")

    tokens.append(Token(TokenKind.EOF, ""))
    return tokens

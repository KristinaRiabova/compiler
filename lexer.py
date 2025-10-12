from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TokenKind(Enum):
    KW_I32 = auto()
    KW_MUT = auto()
    KW_RETURN = auto()
    ID = auto()
    NUMBER = auto()
    LBRACE = auto()
    RBRACE = auto()
    EQ = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    EOF = auto()


@dataclass
class Token:
    kind: TokenKind
    text: str


def simple_lexer(source_tokens: List[str]) -> List[Token]:
    mapping = {
        "i32": TokenKind.KW_I32,
        "mut": TokenKind.KW_MUT,
        "return": TokenKind.KW_RETURN,
        "{": TokenKind.LBRACE,
        "}": TokenKind.RBRACE,
        "=": TokenKind.EQ,
        "+": TokenKind.PLUS,
        "-": TokenKind.MINUS,
        "*": TokenKind.MUL,
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

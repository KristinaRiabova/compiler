from typing import List, Optional
from lexer import Token, TokenKind
from ast_nodes import *


class SyntaxParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.idx = 0

    def peek(self) -> Token:
        return self.tokens[self.idx]

    def eat(self) -> Token:
        cur = self.tokens[self.idx]
        if cur.kind != TokenKind.EOF:
            self.idx += 1
        return cur

    def expect(self, kind: TokenKind) -> Token:
        t = self.peek()
        if t.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {t.kind} ({t.text})")
        return self.eat()

    def parse_program(self) -> ProgramNode:
        stmts: List[StmtNode] = []
        ret_node: Optional[ReturnNode] = None
        while True:
            cur = self.peek()
            if cur.kind == TokenKind.EOF:
                break
            if cur.kind == TokenKind.KW_RETURN:
                if ret_node is not None:
                    raise SyntaxError("Multiple return statements")
                ret_node = self.parse_return()
            else:
                stmt = self.parse_stmt()
                stmts.append(stmt)

            if ret_node is not None and self.peek().kind != TokenKind.EOF:
                raise SyntaxError("Extra tokens after return")

        if ret_node is None:
            raise SyntaxError("No return statement in program")
        return ProgramNode(stmts=stmts, ret=ret_node)

    def parse_stmt(self) -> StmtNode:
        cur = self.peek()
        if cur.kind == TokenKind.KW_I32:
            return self.parse_decl()
        elif cur.kind == TokenKind.ID:
            return self.parse_assign()
        else:
            raise SyntaxError(f"Unexpected token: {cur.text}")

    def parse_decl(self) -> DeclNode:
        self.expect(TokenKind.KW_I32)
        is_mut = False
        if self.peek().kind == TokenKind.KW_MUT:
            is_mut = True
            self.eat()
        idt = self.expect(TokenKind.ID)
        self.expect(TokenKind.LBRACE)
        expr = self.parse_expr()
        self.expect(TokenKind.RBRACE)
        return DeclNode(id_node=IDNode(idt.text), expr=expr, is_mut=is_mut)

    def parse_assign(self) -> AssignNode:
        idt = self.expect(TokenKind.ID)
        self.expect(TokenKind.EQ)
        expr = self.parse_expr()
        return AssignNode(id_node=IDNode(idt.text), expr=expr)

    def parse_return(self) -> ReturnNode:
        self.expect(TokenKind.KW_RETURN)
        expr = self.parse_expr()
        return ReturnNode(expr=expr)

    def parse_expr(self) -> ExprNode:
        left = self.parse_factor()
        cur = self.peek()
        if cur.kind in (TokenKind.PLUS, TokenKind.MINUS, TokenKind.MUL):
            op = self.eat().kind
            right = self.parse_factor()
            return BinaryOpNode(op=op, left=left, right=right)
        else:
            return left

    def parse_factor(self) -> FactorNode:
        cur = self.peek()
        if cur.kind == TokenKind.ID:
            return IDNode(self.eat().text)
        elif cur.kind == TokenKind.NUMBER:
            return NumberNode(int(self.eat().text))
        else:
            raise SyntaxError(f"Expected factor, got {cur.text}")

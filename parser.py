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
            raise SyntaxError(f"Expected {kind.name}, got {t.kind.name} ('{t.text}')")
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
                    raise SyntaxError("Multiple return statements at top-level")
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
        if cur.kind in (TokenKind.KW_I32, TokenKind.KW_I64, TokenKind.KW_BOOL):
            return self.parse_decl()
        elif cur.kind == TokenKind.ID:
            return self.parse_assign()
        elif cur.kind == TokenKind.KW_IF:
            return self.parse_if()
        else:
            raise SyntaxError(f"Unexpected token in statement start: {cur}")

    def parse_decl(self) -> DeclNode:
        type_token = self.eat()
        type_name = {
            TokenKind.KW_I32: "i32",
            TokenKind.KW_I64: "i64",
            TokenKind.KW_BOOL: "bool",
        }[type_token.kind]

        is_mut = False
        if self.peek().kind == TokenKind.KW_MUT:
            is_mut = True
            self.eat()

        idt = self.expect(TokenKind.ID)
        self.expect(TokenKind.LBRACE)
        expr = self.parse_expr()
        self.expect(TokenKind.RBRACE)
        return DeclNode(id_node=IDNode(idt.text), expr=expr, is_mut=is_mut, var_type=type_name)

    def parse_assign(self) -> AssignNode:
        idt = self.expect(TokenKind.ID)
        self.expect(TokenKind.ASSIGN)
        expr = self.parse_expr()
        return AssignNode(id_node=IDNode(idt.text), expr=expr)

    def parse_if(self) -> IfNode:
        self.expect(TokenKind.KW_IF)
        cond = self.parse_expr()
        then_block = self.parse_code_block()
        else_block = None
        if self.peek().kind == TokenKind.KW_ELSE:
            self.eat()
            else_block = self.parse_code_block()
        return IfNode(condition=cond, then_block=then_block, else_block=else_block)

    def parse_code_block(self) -> CodeBlockNode:
        self.expect(TokenKind.LBRACE)
        stmts: List[StmtNode] = []
        ret: Optional[ReturnNode] = None
        while self.peek().kind not in (TokenKind.RBRACE, TokenKind.EOF):
            if self.peek().kind == TokenKind.KW_RETURN:
                ret = self.parse_return()
            else:
                stmts.append(self.parse_stmt())
        self.expect(TokenKind.RBRACE)
        return CodeBlockNode(stmts=stmts, ret=ret)

    def parse_return(self) -> ReturnNode:
        self.expect(TokenKind.KW_RETURN)
        expr = self.parse_expr()
        return ReturnNode(expr=expr)



    def parse_expr(self) -> ExprNode:
        return self.parse_equality()

    def parse_equality(self) -> ExprNode:
        node = self.parse_add()
        while self.peek().kind in (TokenKind.EQEQ, TokenKind.NOTEQ):
            op_tok = self.eat()
            right = self.parse_add()
            node = BinaryOpNode(op=op_tok.kind, left=node, right=right)
        return node

    def parse_add(self) -> ExprNode:
        node = self.parse_mul()
        while self.peek().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op_tok = self.eat()
            right = self.parse_mul()
            node = BinaryOpNode(op=op_tok.kind, left=node, right=right)
        return node

    def parse_mul(self) -> ExprNode:
        node = self.parse_unary()
        while self.peek().kind == TokenKind.MUL:
            op_tok = self.eat()
            right = self.parse_unary()
            node = BinaryOpNode(op=op_tok.kind, left=node, right=right)
        return node

    def parse_unary(self) -> ExprNode:
        if self.peek().kind == TokenKind.NOT:
            self.eat()
            expr = self.parse_unary()
            return NotNode(expr)
        return self.parse_factor()

    def parse_factor(self) -> FactorNode:
        cur = self.peek()
        if cur.kind == TokenKind.ID:
            return IDNode(self.eat().text)
        elif cur.kind == TokenKind.NUMBER:
            return NumberNode(int(self.eat().text))
        elif cur.kind == TokenKind.TRUE:
            self.eat()
            return BoolNode(True)
        elif cur.kind == TokenKind.FALSE:
            self.eat()
            return BoolNode(False)
        else:
            raise SyntaxError(f"Expected factor, got {cur.kind.name} ('{cur.text}')")

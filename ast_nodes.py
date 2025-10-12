from dataclasses import dataclass
from typing import List
from lexer import TokenKind


class ASTNode:
    def visit(self):
        raise NotImplementedError


@dataclass
class ExprNode(ASTNode):
    pass


@dataclass
class FactorNode(ExprNode):
    pass


@dataclass
class IDNode(FactorNode):
    name: str
    def visit(self):
        assert self.name, "Empty identifier"


@dataclass
class NumberNode(FactorNode):
    value: int
    def visit(self):
        pass


@dataclass
class BinaryOpNode(ExprNode):
    op: TokenKind
    left: ExprNode
    right: ExprNode
    def visit(self):
        self.left.visit()
        self.right.visit()
        assert self.op in (TokenKind.PLUS, TokenKind.MINUS, TokenKind.MUL)


class StmtNode(ASTNode):
    pass


@dataclass
class DeclNode(StmtNode):
    id_node: IDNode
    expr: ExprNode
    is_mut: bool
    def visit(self):
        self.id_node.visit()
        self.expr.visit()


@dataclass
class AssignNode(StmtNode):
    id_node: IDNode
    expr: ExprNode
    def visit(self):
        self.id_node.visit()
        self.expr.visit()


@dataclass
class ReturnNode(ASTNode):
    expr: ExprNode
    def visit(self):
        self.expr.visit()


@dataclass
class ProgramNode(ASTNode):
    stmts: List[StmtNode]
    ret: ReturnNode
    def visit(self):
        for s in self.stmts:
            s.visit()
        self.ret.visit()

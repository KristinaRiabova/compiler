from dataclasses import dataclass
from typing import List, Optional
from lexer import TokenKind


class ASTNode:
    def accept(self, visitor):
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
    def accept(self, visitor):
        return visitor.visitID(self)


@dataclass
class NumberNode(FactorNode):
    value: int
    def accept(self, visitor):
        return visitor.visitNumber(self)


@dataclass
class BoolNode(FactorNode):
    value: bool
    def accept(self, visitor):
        return visitor.visitBool(self)


@dataclass
class NotNode(ExprNode):
    expr: ExprNode
    def accept(self, visitor):
        return visitor.visitNot(self)


@dataclass
class BinaryOpNode(ExprNode):
    op: TokenKind
    left: ExprNode
    right: ExprNode
    def accept(self, visitor):
        return visitor.visitBinaryOp(self)


# ============ Statements / Blocks / Program ============

class StmtNode(ASTNode):
    pass


@dataclass
class DeclNode(StmtNode):
    id_node: IDNode
    expr: ExprNode
    is_mut: bool = False
    var_type: str = None
    def accept(self, visitor):
        return visitor.visitDecl(self)


@dataclass
class AssignNode(StmtNode):
    id_node: IDNode
    expr: ExprNode
    def accept(self, visitor):
        return visitor.visitAssign(self)


@dataclass
class ReturnNode(ASTNode):
    expr: ExprNode
    def accept(self, visitor):
        return visitor.visitReturn(self)


@dataclass
class CodeBlockNode(ASTNode):
    stmts: List[StmtNode]
    ret: Optional[ReturnNode] = None
    def accept(self, visitor):
        return visitor.visitCodeBlock(self)


@dataclass
class IfNode(StmtNode):
    condition: ExprNode
    then_block: CodeBlockNode
    else_block: Optional[CodeBlockNode] = None
    def accept(self, visitor):
        return visitor.visitIf(self)


@dataclass
class ProgramNode(ASTNode):
    stmts: List[StmtNode]
    ret: ReturnNode
    def accept(self, visitor):
        return visitor.visitProgram(self)

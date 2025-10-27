from visitor import ASTVisitor
from ast_nodes import *
from typing import Dict, List, Tuple


class SemanticChecker(ASTVisitor):

    def __init__(self):
        self.scopes: List[Dict[str, Tuple[str, bool]]] = [ {} ] 

 
    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def declare(self, name: str, type_str: str, is_mut: bool):
        self.scopes[-1][name] = (type_str, is_mut)

    def lookup(self, name: str) -> Tuple[str, bool]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Undefined variable '{name}'")



    def visitProgram(self, node):
        for s in node.stmts:
            s.accept(self)
        node.ret.accept(self)

    def visitReturn(self, node):
        node.expr.accept(self)

    def visitDecl(self, node: DeclNode):
        expr_type = node.expr.accept(self)

        if node.var_type == "i32" and expr_type == "i64":
            raise Exception(f"Cannot initialize i32 with i64 for '{node.id_node.name}'")
        self.declare(node.id_node.name, node.var_type, node.is_mut)
        return node.var_type

    def visitAssign(self, node: AssignNode):
        left_type, is_mut = self.lookup(node.id_node.name)
        if not is_mut:
            raise Exception(f"Cannot assign to immutable variable '{node.id_node.name}'")
        right_type = node.expr.accept(self)
        if left_type == "i32" and right_type == "i64":
            raise Exception(f"Cannot assign i64 to i32 variable '{node.id_node.name}'")
        return left_type

    def visitIf(self, node: IfNode):
        cond_type = node.condition.accept(self)
        if cond_type != "bool":
            raise Exception("Condition in if-statement must be bool")
        node.then_block.accept(self)
        if node.else_block:
            node.else_block.accept(self)

    def visitCodeBlock(self, node: CodeBlockNode):
        self.push_scope()
        for s in node.stmts:
            s.accept(self)
        if node.ret:
            node.ret.accept(self)
        self.pop_scope()

    def visitNot(self, node: NotNode):
        typ = node.expr.accept(self)
        if typ != "bool":
            raise Exception("Negation operator '!' can only be applied to bool")
        return "bool"

    def visitBinaryOp(self, node: BinaryOpNode):
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)

        if node.op in (TokenKind.PLUS, TokenKind.MINUS, TokenKind.MUL):
            if "i64" in (left_type, right_type):
                return "i64"
            if left_type in ("i32",) and right_type in ("i32",):
                return "i32"
            raise Exception("Arithmetic operators require integer operands")

        elif node.op in (TokenKind.EQEQ, TokenKind.NOTEQ):
            
            if left_type == right_type:
                return "bool"
            if {left_type, right_type} <= {"i32", "i64"}:
                return "bool"
            raise Exception("Cannot compare incompatible types")
        else:
            raise Exception(f"Unknown operator {node.op}")

    def visitID(self, node: IDNode):
        ty, _ = self.lookup(node.name)
        return ty

    def visitNumber(self, node: NumberNode):
        return "i32"

    def visitBool(self, node: BoolNode):
        return "bool"

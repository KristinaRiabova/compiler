from visitor import ASTVisitor
from ast_nodes import *

class SemanticChecker(ASTVisitor):
    def __init__(self):
        self.symbols = {}

    def visitProgram(self, node):
        for s in node.stmts:
            s.accept(self)
        node.ret.accept(self)

    def visitReturn(self, node):
        node.expr.accept(self)

    def visitDecl(self, node):
        var_name = node.id_node.name
        expr_type = node.expr.accept(self)
        self.symbols[var_name] = expr_type
        return expr_type
    

    

    def visitAssign(self, node):
        var_name = node.id_node.name
        if var_name not in self.symbols:
            raise Exception(f"Undefined variable '{var_name}'")
        left_type = self.symbols[var_name]
        right_type = node.expr.accept(self)
        if left_type == "i32" and right_type == "i64":
            raise Exception(f"Cannot assign i64 to i32 variable '{var_name}'")
        return left_type

    def visitBinaryOp(self, node):
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)

        if node.op.name in ["PLUS", "MINUS", "MUL"]:
            if "i64" in (left_type, right_type):
                return "i64"
            return "i32"

        elif node.op.name in ["EQEQ", "NOTEQ"]:
            return "bool"

        else:
            raise Exception(f"Unknown operator {node.op}")

    def visitID(self, node):
        if node.name not in self.symbols:
            raise Exception(f"Undefined variable '{node.name}'")
        return self.symbols[node.name]


    def visitNumber(self, node):
        return "i32"
    
    def visitBool(self, node):
        return "bool"



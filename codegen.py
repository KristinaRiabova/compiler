
from visitor import ASTVisitor
from ast_nodes import *

class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.output = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"%t{self.temp_count}"

    def visitProgram(self, node):
        for s in node.stmts:
            s.accept(self)
        node.ret.accept(self)
        print("\n".join(self.output))

    def visitDecl(self, node):
        val = node.expr.accept(self)
        self.output.append(f"{node.id_node.name} = {val}")

    def visitAssign(self, node):
        val = node.expr.accept(self)
        self.output.append(f"{node.id_node.name} = {val}")

    def visitReturn(self, node):
        val = node.expr.accept(self)
        self.output.append(f"ret {val}")

    def visitBinaryOp(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        temp = self.new_temp()
        op_map = {
            "PLUS": "add",
            "MINUS": "sub",
            "MUL": "mul",
            "EQEQ": "eq",
            "NOTEQ": "ne"
        }
        op = op_map[node.op.name]
        self.output.append(f"{temp} = {op} {left}, {right}")
        return temp

    def visitID(self, node):
        return node.name

    def visitNumber(self, node):
        return str(node.value)


    def visitBool(self, node):
        return "true" if node.value else "false"

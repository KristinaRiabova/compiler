from visitor import ASTVisitor
from ast_nodes import *
from lexer import TokenKind


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.output = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"%t{self.temp_count}"

    def new_label(self, base: str):
        self.label_count += 1
        return f"{base}_{self.label_count}"



    def visitProgram(self, node: ProgramNode):
        for s in node.stmts:
            s.accept(self)
        node.ret.accept(self)
        print("\n".join(self.output))

    def visitDecl(self, node: DeclNode):
        val = node.expr.accept(self)
        self.output.append(f"{node.id_node.name} = {val}")

    def visitAssign(self, node: AssignNode):
        val = node.expr.accept(self)
        self.output.append(f"{node.id_node.name} = {val}")

    def visitReturn(self, node: ReturnNode):
        val = node.expr.accept(self)
        self.output.append(f"ret {val}")

    def visitIf(self, node: IfNode):
        cond = node.condition.accept(self)
        lbl_else = self.new_label("L_else")
        lbl_end = self.new_label("L_end")
        # branch-if-false to else
        self.output.append(f"br_if_false {cond}, {lbl_else}")
        node.then_block.accept(self)
        self.output.append(f"jmp {lbl_end}")
        self.output.append(f"{lbl_else}:")
        if node.else_block:
            node.else_block.accept(self)
        self.output.append(f"{lbl_end}:")

    def visitCodeBlock(self, node: CodeBlockNode):
        for s in node.stmts:
            s.accept(self)
        if node.ret:
            node.ret.accept(self)

    def visitNot(self, node: NotNode):
        val = node.expr.accept(self)
        t = self.new_temp()
        self.output.append(f"{t} = not {val}")
        return t

    def visitBinaryOp(self, node: BinaryOpNode):
        left = node.left.accept(self)
        right = node.right.accept(self)
        temp = self.new_temp()
        op_map = {
            TokenKind.PLUS: "add",
            TokenKind.MINUS: "sub",
            TokenKind.MUL: "mul",
            TokenKind.EQEQ: "eq",
            TokenKind.NOTEQ: "ne",
        }
        op = op_map[node.op]
        self.output.append(f"{temp} = {op} {left}, {right}")
        return temp

    def visitID(self, node: IDNode):
        return node.name

    def visitNumber(self, node: NumberNode):
        return str(node.value)

    def visitBool(self, node: BoolNode):
        return "true" if node.value else "false"

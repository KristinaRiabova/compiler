from lexer import simple_lexer
from parser import SyntaxParser
from semantic_checker import SemanticChecker
from codegen import CodeGenerator

if __name__ == "__main__":
    code = [
        "i32", "mut", "a", "{", "10", "}",
        "bool", "mut", "b", "{", "true", "}",
        "if", "!", "b",
        "{",
            "a", "=", "a", "+", "5",
        "}",
        "else",
        "{",
            "i64", "mut", "a", "{", "20", "}",
            "return", "a",
        "}",
        "return", "a",
    ]

    tokens = simple_lexer(code)
    parser = SyntaxParser(tokens)
    program = parser.parse_program()

    print(" AST + Semantic checks ")
    sema = SemanticChecker()
    program.accept(sema)

    print("\n IR ")
    codegen = CodeGenerator()
    program.accept(codegen)

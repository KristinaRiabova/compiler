from lexer import simple_lexer
from parser import SyntaxParser
from semantic_checker import SemanticChecker
from codegen import CodeGenerator

if __name__ == "__main__":
    code = ["i64", "a", "{", "10", "}", "bool", "b", "{", "true", "}", "return", "a"]

    tokens = simple_lexer(code)
    parser = SyntaxParser(tokens)
    program = parser.parse_program()

    print(" AST ")
    sema = SemanticChecker()
    program.accept(sema)

    print("")
    codegen = CodeGenerator()
    program.accept(codegen)

from lexer import simple_lexer
from parser import SyntaxParser

if __name__ == "__main__":
   
   
    sample_code = ["i32", "x", "{", "10", "}", "y", "=", "x", "+", "5", "return", "y"]

    tokens = simple_lexer(sample_code)
    parser = SyntaxParser(tokens)

    program = parser.parse_program()
    print("\nAST!")
    print(program)

    
    program.visit()
    print(" AST!")

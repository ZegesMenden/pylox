from __future__ import annotations
import io

def tabs(tabCount: int):
    return '\t'*tabCount

def forwardDeclare(file: io.TextIOWrapper, name: str):
    file.write(f"class {name.strip(' ')}:\n")
    file.write(f"{tabs(1)}def accept(self, visitor):\n")
    file.write(f"{tabs(2)}pass\n\n")

def defineVisitor(file: io.TextIOWrapper, basename: str, types: list[str]):
    
    file.write(f"{tabs(1)}class Visitor:\n")

    file.write("\n")
    file.write(f"{tabs(2)}def __init__(self):\n")
    file.write(f"{tabs(3)}pass\n")
    file.write("\n")

    for type in types:
        typename = type.split(":")[0]
        file.write(f"{tabs(2)}def visit{typename.strip(' ')}{basename.strip(' ')}(self, {basename.lower()}: {typename}):\n")
        file.write(f"{tabs(3)}pass\n")
        file.write("\n")

def defineClass(file: io.TextIOWrapper, name: str, basename: str, fields: list[str]):

    tabCount = 0

    file.write(f"class {name.strip(' ')}({basename}):\n")
    file.write("\n")
    tabCount += 1
    file.write(f"{tabs(tabCount)}def __init__(self, {', '.join([field.strip(' ') for field in fields])}):\n")
    tabCount += 1
    for field in fields:
        file.write(f"{tabs(tabCount)}self.{field.strip(' ')} = {field.split(':')[0].strip(' ')}\n")
    tabCount -= 1

    file.write("\n")
    file.write(f"{tabs(tabCount)}def accept(self, visitor):\n")
    tabCount += 1
    file.write(f"{tabs(tabCount)}return visitor.visit{name.strip(' ')}{basename.strip(' ')}(self)\n")

    pass

def generateAST(out_dir: str, basename: str, types: list[str]):
    path = out_dir + ".py"

    with open(path, "w") as file:

        tabCount = 0

        classnames = [type.split(":")[0].strip(" ") for type in types]

        # import plox
        file.write("from __future__ import annotations\n")
        file.write("from plox import Token\n")

        file.write("\n")
        
        # Not needed actually because of annotations
        # for name in classnames:
        #     forwardDeclare(file, name)
        # file.write("\n")
        
        # Generate AST base class
        file.write(f"class {basename}:\n")
        tabCount += 1

        file.write("\n")
        file.write(f"{tabs(tabCount)}def __init__(self):\n")

        tabCount += 1
        file.write(f"{tabs(tabCount)}pass\n")
        tabCount = 0
        file.write("\n")

        tabCount += 1

        defineVisitor(file, basename, classnames)

        for type in types:
            split_str = type.split(":")
            classname = (split_str[0]).strip(" ")

            defineClass(file, classname, basename, type[len(split_str[0])+1:].split(","))
            file.write("\n")


if __name__ == '__main__':
    
    #generateAST("AST", "Expr",  
    #            ["Assign   : name: Token, value: Expr",
    #             "Binary   : left: Expr, operator: Token, right: Expr",
    #             "Call     : callee: Expr, paren: Token, arguments: list[Expr]",
    #             "Get      : object: Expr, name: Token",
    #             "Grouping : expression: Expr",
    #             "Literal  : value: any",
    #             "Logical  : left: Expr, operator: Token, right: Expr",
    #             "Set      : object: Expr, name: Token, value: Expr",
    #             "Super    : keyword: Token, method: Token",
    #             "This     : keyword: Token",
    #             "Unary    : operator: Token, right: Expr",
    #             "Variable : name: Token"])

                
    generateAST("STMT", "Stmt", [
        "Block      : statements: list[Stmt]",
        "Expression : expression: Expr",
        "If         : condition: Expr, thenBranch: Stmt, elseBranch: Stmt",
        "Print      : expression: Expr",
        "Var        : name: Token, initializer: Expr",
        "While      : condition: Expr, body: Stmt"])
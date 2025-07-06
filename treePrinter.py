from AST import *
from ploxTokens import *

class ASTPrinter(Expr.Visitor):

    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr):
        builder = ""
        builder += "(" + name

        for expr in exprs:
            builder += " "
            builder += expr.accept(self)

        builder += ")"

        return builder
    
def main():
    expression = Binary(
        Unary(Token(tokenType.minus, "-", None, 1), Literal(123)),
        Token(tokenType.star, "*", None, 1),
        Grouping(Literal(45.67))
    )

    print(ASTPrinter().print(expression))

if __name__ == '__main__':
    main()
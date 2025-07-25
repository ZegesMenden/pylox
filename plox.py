from __future__ import annotations
from enum import Enum
import sys

from AST import *
from STMT import *
from environment import Environment
from treePrinter import ASTPrinter
from ploxTokens import *

class Scanner:

    def __init__(self, lox_inst: lox, source: str = ""):

        self.lox_inst: lox = lox_inst

        self.source: str = source
        self.tokens: list[Token] = []

        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def addToken(self, type: tokenType, literal: any = None):
        self.tokens.append(Token(type, self.source[self.start:self.current], self.line, literal))

    def match(self, ch):
        if ( self.current < len(self.source) ):
            
            if self.source[self.current] != ch:
                return False
            
            self.current += 1
            return True

        return False

    def peek(self, dist: int = 1):
        if self.current + dist >= len(self.source):
            return '\0'
        return self.source[self.current + dist]

    def advance(self):
        self.current += 1
        if self.current >= len(self.source):
            return '\0'
        return self.source[self.current]

    def scanToken(self):

        def number():
            while self.peek().isnumeric(): self.advance()
            if self.peek() == '.' and self.peek(2).isnumeric():
                self.advance()
                while self.peek().isnumeric(): self.advance()
            self.advance()
            self.addToken(tokenType.number, float(self.source[self.start:self.current-1]))

        def identifier():
            while self.peek().isalnum():
                self.advance()
            self.advance()

            keywordMap = {
                "and": tokenType.AND,
                "class": tokenType.CLASS,
                "else": tokenType.ELSE,
                "false": tokenType.FALSE,
                "fun": tokenType.FUN,
                "for": tokenType.FOR,
                "if": tokenType.IF,
                "nil": tokenType.NIL,
                "or": tokenType.OR,
                "print": tokenType.PRINT,
                "return": tokenType.RETURN,
                "super": tokenType.SUPER,
                "this": tokenType.THIS,
                "true": tokenType.TRUE,
                "var": tokenType.VAR,
                "while": tokenType.WHILE
            }

            text = self.source[self.start:self.current]
            if text in keywordMap:
                self.addToken(keywordMap[text])
            else:
                self.addToken(tokenType.identifier, literal=text)

        c = self.source[self.current]
        self.advance()

        match(c):
            case('('): 
                self.addToken(tokenType.paren_l)
            case(')'): 
                self.addToken(tokenType.paren_r)
            case('{'): 
                self.addToken(tokenType.brace_l)
            case('}'): 
                self.addToken(tokenType.brace_r)
            case(','): 
                self.addToken(tokenType.comma)
            case('.'): 
                self.addToken(tokenType.dot)
            case('-'): 
                self.addToken(tokenType.minus)
            case('+'): 
                self.addToken(tokenType.plus)
            case(';'): 
                self.addToken(tokenType.semicolon)
            case('*'): 
                self.addToken(tokenType.star)
            case('!'):
                self.addToken(tokenType.bang if not self.match('=') else tokenType.bang_equal)
            case('='):
                self.addToken(tokenType.equal if not self.match('=') else tokenType.equal_equal)
            case('<'):
                self.addToken(tokenType.lesser if not self.match('=') else tokenType.lesser_equal)
            case('>'):
                self.addToken(tokenType.greater if not self.match('=') else tokenType.greater_equal)
            case('/'):
                if not self.match('/'):
                    self.addToken(tokenType.slash)
                else:
                    while self.source[self.current] != '\n' and self.current < len(self.source):
                        self.current += 1
            case('\r'):
                pass
            case('\t'):
                pass
            case(' '):
                pass
            case('\n'):
                self.line += 1
                pass
            case('"'):
                self.current += 1
                tmp: str = ""
                while self.current < len(self.source) and self.source[self.current] != '"':
                    tmp += self.source[self.current]
                    if tmp == '\n':
                        self.line += 1
                    self.current += 1
                
                if self.current < len(self.source):
                    self.current += 1

                self.addToken(tokenType.string, tmp)
            case _:
                if c.isnumeric():
                    number()
                elif c.isalpha():
                    identifier()
                else:
                    self.lox_inst.error(self.lox_inst, self.line, "invalid character")

    def scanTokens(self):
        while self.current < len(self.source):
            self.start = self.current
            self.scanToken()
        self.addToken(tokenType.EOF)
        return self.tokens

class ParserError(RuntimeError):
    pass
    
class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, msg: str):
        super().__init__(msg)
        self.token = token
        self.msg = msg

class Parser:

    def __init__(self, lox_inst: lox, tokens: list[Token]):
        self.lox_inst: lox = lox_inst
        self.tokens: list[Token] = tokens
        self.current: int = 0

    def error(self, tok: Token, msg: str):
        self.lox_inst.error(tok, msg)
        raise ParserError

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def isAtEnd(self) -> bool:
        return self.peek().type == tokenType.EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def check(self, type: tokenType) -> bool:
        if self.isAtEnd():
            return False
        else:
            # print(f"check {self.peek().type} == {type} ? {self.peek().type == type}")
            return self.peek().type == type

    def consume(self, type: tokenType, message: str):
        if self.check(type): return self.advance()
        self.error(self.peek(), message)

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():

            if self.previous().type == tokenType.semicolon:
                return
            
            if self.peek().type not in [
                tokenType.CLASS,
                tokenType.FUN,
                tokenType.FOR,
                tokenType.VAR,
                tokenType.IF,
                tokenType.WHILE,
                tokenType.PRINT,
                tokenType.RETURN]:
                return
            
            self.advance()

    def match(self, tokenTypes: list[tokenType]|tokenType) -> bool:
        if isinstance(tokenTypes, tokenType):
            if self.check(tokenTypes):
                self.advance()
                return True
        else:
            for type in tokenTypes:
                if self.check(type):
                    self.advance()
                    return True
        return False

    def And(self):
        expr = self.equality()

        while self.match(tokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def Or(self):
        expr = self.And()

        while self.match(tokenType.OR):
            operator = self.previous()
            right = self.And()
            expr = Logical(expr, operator, right)

        return expr

    def assignment(self):
        expr = self.Or()

        if self.match(tokenType.equal):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            
            self.error(equals, "Bad assignment target.")

        return expr

    def expression(self):
        return self.assignment()

    def equality(self) -> Expr:
        expr = self.comparrison()

        while self.match([tokenType.bang_equal, tokenType.equal_equal]):
            operator: Token = self.previous()
            right: Expr = self.comparrison()
            expr = Binary(expr, operator, right)

        return expr

    def comparrison(self) -> Expr:
        expr = self.term()

        while self.match([tokenType.greater, tokenType.greater_equal, tokenType.lesser, tokenType.lesser_equal]):
            operator: Token = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match([tokenType.minus, tokenType.plus]):
            operator: Token = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match([tokenType.slash, tokenType.star]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match([tokenType.bang, tokenType.minus]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()

    def primary(self):

        if self.match([tokenType.FALSE]): return Literal(False)
        if self.match([tokenType.TRUE]): return Literal(True)
        if self.match([tokenType.NIL]): return Literal(tokenType.NIL)

        if self.match([tokenType.string, tokenType.number]):
            return Literal(self.previous().literal)
    
        if self.match([tokenType.identifier]):
            return Variable(self.previous())
    
        if self.match([tokenType.paren_l]):
            expr = self.expression()
            self.consume(tokenType.paren_r, "expected ')' after expression")
            return Grouping(expr)

        self.error(self.peek(), "expected expression")

    def __printStatement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(tokenType.semicolon, "Expect ; after value.")
        return Print(value)
    
    def __expressionStatement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(tokenType.semicolon, "Expect ; after expression.")
        return Expression(expr)
    
    def __block(self):
        statements = []

        while (not self.check(tokenType.brace_r)) and (not self.isAtEnd()):
            statements.append(self.__declaration())

        self.consume(tokenType.brace_r, "icl you need a } somewhere here.")
        return statements

    def __ifStatement(self):
        self.consume(tokenType.paren_l, "where's the ( after 'if'?")
        condition = self.expression()
        self.consume(tokenType.paren_r, "hey twin, i think you forgot the ) after your condition")

        thenBranch = self.__statement()
        elseBranch = None
        if self.match(tokenType.ELSE):
            elseBranch = self.__statement()
        
        return If(condition, thenBranch, elseBranch)

    def __whileStatement(self):

        self.consume(tokenType.paren_l, "errm, twinnum... i think you forgot a '(' after while")
        condition = self.expression()
        self.consume(tokenType.paren_r, "ok atp this has to be intentional bruh, where's the ')' after your condition")

        body = self.__statement()

        return While(condition, body)

    def __forStatement(self):

        self.consume(tokenType.paren_l, "twin... how are you forgetting your '(' before the for loop...")
        initializer = None

        if self.match(tokenType.semicolon):
            initializer = None
        elif self.match(tokenType.VAR):
            initializer = self.__varDeclaration()
        else:
            initializer = self.__expressionStatement()
        
        condition: Expr = None
        if not self.check(tokenType.semicolon):
            condition = self.expression()
        self.consume(tokenType.semicolon, "are we fr. where the FUCK is your ';' following the loop condition")

        increment = None
        if not self.check(tokenType.paren_r):
            increment = self.expression()

        self.consume(tokenType.paren_r, "come on man, where's the ')' after your clauses")

        body = self.__statement()

        if increment is not None:
            body = Block(
                [body, Expression(increment)]
            )

        if condition is None:
            condition = Literal(True)
        
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body


    def __statement(self) -> Stmt:
        if self.match([tokenType.FOR]): return self.__forStatement()
        if self.match([tokenType.IF]): return self.__ifStatement()
        if self.match([tokenType.PRINT]): return self.__printStatement()
        if self.match([tokenType.WHILE]): return self.__whileStatement()
        if self.match([tokenType.brace_l]): return Block(self.__block())
        
        return self.__expressionStatement()

    def __declaration(self) -> Stmt:
        try:
            if self.match([tokenType.VAR]):
                return self.__varDeclaration()
            return self.__statement()
        except ParserError as err:
            self.synchronize()
            raise err
    
    def __varDeclaration(self) -> Stmt:
        name: Token = self.consume(tokenType.identifier, "Expecte variable name! ts pmo...");
        
        initializer = None
        if self.match([tokenType.equal]):
            initializer = self.expression()
    
        self.consume(tokenType.semicolon, "SYBAU And add a semicolon (;) after variable declaration bruh")
        
        return Var(name, initializer)
    
    def parse(self):
        
        statements: list[Stmt] = []
        
        while not self.isAtEnd():
            statements.append(self.__declaration())
        
        return statements

class Interpreter(Expr.Visitor, Stmt.Visitor):

    def __init__(self, lox_inst: lox):
        self.lox_inst: lox = lox_inst
        self.environment: Environment = Environment()
    
    def visitWhileStmt(self, stmt):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.type == tokenType.OR:
            if self.isTruthy(left): return left
        else:
            if not self.isTruthy(left): return left
        
        return self.evaluate(expr.right)

    def visitIfStmt(self, stmt: If):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visitBlockStmt(self, stmt):
        self.__executeBlock(stmt.statements, Environment(self.environment))

    def __executeBlock(self, statements: list[Stmt], environment: Environment):
        previous: Environment = self.environment

        try:

            self.environment = environment
            for statement in statements:
                self.execute(statement)
            
        finally:
            self.environment = previous

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visitVarStmt(self, stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visitVariableExpr(self, expr: Variable):
        return self.environment.get(expr.name)

    def visitExpressionStmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)
        
    def visitPrintStmt(self, stmt: Print):
        val = self.evaluate(stmt.expression)
        print(self.stringify(val))

    def visitLiteralExpr(self, expr: Literal):
        return expr.value
    
    def visitGroupingExpr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)
        
        match(right.operator.type):
            case(tokenType.minus):
                return -float(right)
            case(tokenType.bang):
                return not self.isTruthy(right)
        return None

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match(expr.operator.type):
            case(tokenType.minus):
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) - float(right)
            case(tokenType.slash):
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) / float(right)
            case(tokenType.star):
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) * float(right)
            case(tokenType.plus):
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                
                raise LoxRuntimeError(expr.operator, "operands must be two numbers or strings")
            
            case(tokenType.greater):
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) > float(right)
            case(tokenType.greater_equal):
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) >= float(right)
            case(tokenType.lesser):
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) < float(right)
            case(tokenType.lesser_equal):
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) <= float(right)
            
            case(tokenType.bang_equal):
                return not self.isEqual(left, right)
            case(tokenType.equal):
                return self.isEqual(left, right)
            
        return None

    def checkNumberOperand(self, operator: Token, operand: object):
        if isinstance(operand, float): return
        raise LoxRuntimeError(operator, "operand must be a number")

    def checkNumberOperands(self, operator: Token, left: object, right: object):
        if isinstance(left, float) and isinstance(right, float): return
        raise LoxRuntimeError(operator, "operand must be a number")

    def isEqual(self, left: object, right: object) -> bool:
        if left is None and right is None: return True
        if left is None: return False

        return left == right

    def isTruthy(self, obj: object) -> bool:
        if obj is None: return False
        if isinstance(obj, bool): return bool(obj)
        return True

    def stringify(self, value: object):
        if value is None: return "nil"

        if isinstance(value, float):
            return f"{round(value, 2)}"

        return str(value)
    
    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def interperate(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as e:
            self.lox_inst.runTimeError(e)
        except Exception as e:
            raise e

class lox:

    def __init__(self, lexOut: str = "") -> None:
        self.hasError = False
        self.hasRunTimeError = False
        self.lexOut: str = lexOut
        self.interpreter: Interpreter = Interpreter(self)
        pass

    def report(self, line: int, where: str, msg: str):
        print(f"[line {line}] Error {where}: {msg}")
        self.hasError = True

    def error(self, tok: Token, msg: str):
        if tok.type == tokenType.EOF:
            self.report(tok.line, " at end", msg)
        else:
            self.report(tok.line, f"at '{tok.lexeme}'", msg)

    def runTimeError(self, err: LoxRuntimeError):
        print(f"{err.msg}\n[line {err.token.line}]")
        self.hasRunTimeError = True

    def run(self, line: str):
        scanner = Scanner(self, line)
        tokens = scanner.scanTokens()
        
        parser = Parser(self, tokens)

        try:
            statements = parser.parse()
        except ParserError as err:
            print(f"Parsing error: {err}")
            return
        
        if self.hasError:
            self.hasError = False
            return
        
        self.interpreter.interperate(statements)

        if self.hasRunTimeError:
            self.hasRunTimeError = False
            return

    def runPrompt(self):
        while True:
            inp = ""
            try:
                inp = input(">> ")
            except EOFError:
                return
            self.run(inp)
            
    def runFile(self, fname: str):

        with open(fname, "r") as f:
            for line in f.readlines():
                self.run(line)

if __name__ == '__main__':
    
    interp = lox("lexout.txt")

    if len(sys.argv) > 1:
        interp.runFile(sys.argv[1])
    else:
        interp.runPrompt()
    
    if interp.hasError:
        exit(65)

    if interp.hasRunTimeError:
        exit(70)
    
    exit(0)

from enum import Enum
import sys

class tokenType(Enum):

    notok = 0

    paren_l = 1
    paren_r = 2
    brace_l = 3
    brace_r = 4

    comma = 5
    dot = 6
    minus = 7
    plus = 39
    semicolon = 8
    slash = 9
    star = 10

    bang = 11
    bang_equal = 12

    equal = 13
    equal_equal = 14
    greater = 15
    greater_equal = 16
    lesser = 17
    lesser_equal = 18

    identifier = 19
    string = 20
    number = 21

    AND = 22
    CLASS = 23
    ELSE = 24
    FALSE = 25
    FUN = 26
    FOR = 27
    IF = 28
    NIL = 29
    OR = 30
    PRINT = 31
    RETURN = 32
    SUPER = 33
    THIS = 34
    TRUE = 35
    VAR = 36
    WHILE = 37

    EOF = 38
    
class Token:

    def __init__(self, type = tokenType.notok, lexeme: str = "", line: int = 0, literal: any = None):

        self.type: tokenType = type
        self.lexeme: str = lexeme
        self.literal: any = literal
        self.line: int = line

        pass

    def __str__(self):
        return f"""token: [{(str(self.type).removeprefix('tokenType.'))}] lex: [{self.lexeme}] literal: [{str(self.literal)}]"""

    def __repr__(self):
        return str(self)
        
class Scanner:

    def __init__(self, source: str = ""):

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
            self.addToken(tokenType.number, float(self.source[self.start:self.current]))

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
                while self.source[self.current] != '"' and self.current < len(self.source):
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
                    lox.error(lox_inst, self.line, "invalid character")

    def scanTokens(self):
        while self.current < len(self.source):
            self.start = self.current
            self.scanToken()
        self.addToken(tokenType.EOF)
        return self.tokens

class lox:

    def __init__(self, lexOut: str = "") -> None:
        self.hasError = False
        self.lexOut: str = lexOut
        pass

    def report(self, line, where, msg):
        print(f"[line {line}] Error {where}: {msg}")
        self.hasError = True

    def error(self, line, msg):
        self.report(line, "", msg)

    def run(self, line: str):
        scanner = Scanner(line)
        tokens = scanner.scanTokens()
        if self.lexOut != "":
            with open(self.lexOut, "a+") as f:
                f.write(", ".join(tokens))
        pass

    def runPrompt(self):
        while True:
            inp = input(">> ")
            if inp == "":
                return
            self.run(inp)
            
    def runFile(self, fname: str):

        with open(fname, "r") as f:
            for line in f.readlines():
                self.run(line)

lox_inst: lox = lox("lexout.txt")

if __name__ == '__main__':
    interp = lox_inst
    if len(sys.argv) > 1:
        interp.runFile(sys.argv[1])
    else:
        interp.runPrompt()
    
    if interp.hasError:
        exit(65)
    exit(0)

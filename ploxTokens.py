from enum import Enum


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

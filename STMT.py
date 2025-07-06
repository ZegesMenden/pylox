from __future__ import annotations
from AST import Token, Expr

class Stmt:

	def __init__(self):
		pass

	class Visitor:

		def __init__(self):
			pass

		def visitExpressionStmt(self, stmt: Expression):
			pass

		def visitPrintStmt(self, stmt: Print):
			pass

		def visitVarStmt(self, stmt: Var):
			pass

	def accept(self, visitor: Stmt.Visitor):
		pass

class Expression(Stmt):

	def __init__(self, expression: Expr):
		self.expression: Expr = expression

	def accept(self, visitor: Stmt.Visitor):
		return visitor.visitExpressionStmt(self)

class Print(Stmt):

	def __init__(self, expression: Expr):
		self.expression: Expr = expression

	def accept(self, visitor: Stmt.Visitor):
		return visitor.visitPrintStmt(self)

class Var(Stmt):

	def __init__(self, name: Token, initializer: Expr|None):
		self.name: Token = name
		self.initializer: Expr|None = initializer

	def accept(self, visitor: Stmt.Visitor):
		return visitor.visitVarStmt(self)


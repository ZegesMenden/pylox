from __future__ import annotations
from AST import Token, Expr

class Stmt:

	def __init__(self):
		pass

	def accept(self, visitor: Stmt.Visitor):
		pass

	class Visitor:

		def __init__(self):
			pass

		def visitBlockStmt(self, stmt: Block):
			pass

		def visitExpressionStmt(self, stmt: Expression):
			pass

		def visitIfStmt(self, stmt: If):
			pass

		def visitPrintStmt(self, stmt: Print):
			pass

		def visitVarStmt(self, stmt: Var):
			pass

		def visitWhileStmt(self, stmt: While):
			pass

class Block(Stmt):

	def __init__(self, statements: list[Stmt]):
		self.statements: list[Stmt] = statements

	def accept(self, visitor: Stmt.Visitor):
		return visitor.visitBlockStmt(self)

class Expression(Stmt):

	def __init__(self, expression: Expr):
		self.expression: Expr = expression

	def accept(self, visitor: Stmt.Visitor):
		return visitor.visitExpressionStmt(self)

class If(Stmt):

	def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt):
		self.condition: Expr = condition
		self.thenBranch: Stmt = thenBranch
		self.elseBranch: Stmt = elseBranch

	def accept(self, visitor: Stmt.Visitor):
		return visitor.visitIfStmt(self)

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

class While(Stmt):

	def __init__(self, condition: Expr, body: Stmt):
		self.condition: Expr = condition
		self.body: Stmt = body

	def accept(self, visitor: Stmt.Visitor):
		return visitor.visitWhileStmt(self)


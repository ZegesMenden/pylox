from __future__ import annotations
from ploxTokens import *

class Expr:

	def __init__(self):
		pass

	class Visitor:

		def __init__(self):
			pass

		def visitAssignExpr(self, expr: Assign) -> object:
			pass

		def visitBinaryExpr(self, expr: Binary) -> object:
			pass

		def visitCallExpr(self, expr: Call) -> object:
			pass

		def visitGetExpr(self, expr: Get) -> object:
			pass

		def visitGroupingExpr(self, expr: Grouping) -> object:
			pass

		def visitLiteralExpr(self, expr: Literal) -> object:
			pass

		def visitLogicalExpr(self, expr: Logical) -> object:
			pass

		def visitSetExpr(self, expr: Set) -> object:
			pass

		def visitSuperExpr(self, expr: Super) -> object:
			pass

		def visitThisExpr(self, expr: This) -> object:
			pass

		def visitUnaryExpr(self, expr: Unary) -> object:
			pass

		def visitVariableExpr(self, expr: Variable) -> object:
			pass

	def accept(self, visitor: Expr.Visitor) -> object:
		pass

class Assign(Expr):

	def __init__(self, name: Token, value: Expr):
		self.name: Token = name
		self.value: Expr = value

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitAssignExpr(self)

class Binary(Expr):

	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left: Expr = left
		self.operator: Token = operator
		self.right: Expr = right

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitBinaryExpr(self)

class Call(Expr):

	def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]):
		self.callee: Expr = callee
		self.paren: Token = paren
		self.arguments: list[Expr] = arguments

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitCallExpr(self)

class Get(Expr):

	def __init__(self, object: Expr, name: Token):
		self.object: Expr = object
		self.name: Token = name

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitGetExpr(self)

class Grouping(Expr):

	def __init__(self, expression: Expr):
		self.expression: Expr = expression

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitGroupingExpr(self)

class Literal(Expr):

	def __init__(self, value: object):
		self.value: object = value

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitLiteralExpr(self)

class Logical(Expr):

	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left: Expr = left
		self.operator: Token = operator
		self.right: Expr = right

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitLogicalExpr(self)

class Set(Expr):

	def __init__(self, object: Expr, name: Token, value: Expr):
		self.object: Expr = object
		self.name: Token = name
		self.value: Expr = value

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitSetExpr(self)

class Super(Expr):

	def __init__(self, keyword: Token, method: Token):
		self.keyword: Token = keyword
		self.method: Token = method

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitSuperExpr(self)

class This(Expr):

	def __init__(self, keyword: Token):
		self.keyword: Token = keyword

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitThisExpr(self)

class Unary(Expr):

	def __init__(self, operator: Token, right: Expr):
		self.operator: Token = operator
		self.right: Expr = right

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitUnaryExpr(self)

class Variable(Expr):

	def __init__(self, name: Token):
		self.name: Token = name

	def accept(self, visitor: Expr.Visitor) -> object:
		return visitor.visitVariableExpr(self)


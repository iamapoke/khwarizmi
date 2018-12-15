"""Basic expressions"""

from khwarizmi.misc import if_assign, is_number
from khwarizmi.exc import NoVariableError
import copy

SEPARATORS = ['+', '-', '=', '*', "(", ")"]
excused_symbols = ["/", "."]


class Expression:

	def __init__(self, expression):
		self.expression = expression.replace(' ', '')
		self.variables = self.get_variables()
		self.unknown = self.variables[0]
		self.terms = self.get_terms()
		self.coefficients = self.get_coefficients()

	def get_variables(self):
		"""Adds every variable of the equation
		to the variables attribute (list)."""

		index, incs = 0, []
		for symbol in self.expression:

			if symbol.isalpha() and symbol not in incs:
				incs.append(symbol)

		if len(incs) is 0:
			raise NoVariableError(self.expression)

		return incs

	def get_number(self, index, expression=None, catch_variable=False, catch_term=False):

		expression = self.expression if expression is None else expression
		catcher = copy.copy(SEPARATORS)
		is_negative = False

		if catch_term is True and catch_variable is False:
			catch_variable = True

		if catch_variable is False:
			catcher.extend(self.variables)
		if catch_term is True:
			catcher.remove('*')

		expression = expression[index:]
		if expression.startswith('-'):
			is_negative = True
			expression = expression[1:]

		if any(x in catcher for x in expression):
			separator = next((x for x in expression if x in catcher))
			pos = expression.find(separator)
			if expression[0:pos] is "" and is_number(expression[0:pos+1]):
				number = expression[0:pos+1]
			else:
				number = expression[0:pos]
		else:
			number = expression

		return number if is_negative is False else '-' + number

	def get_terms(self, side=None):
		"""Returns a list of all terms of this equation."""

		side = self.expression if side is None else side
		index, terms = 0, []

		while index < len(side):
			term = self.get_number(index, side, catch_term=True)
			if len(term) > 0:
				terms.append(term)
			index += len(term) if len(term) > 0 else 1
		return terms

	def get_coefficients(self):

		coefficients = []

		for term in self.terms:
			if any(char.isalpha() for char in term):
				coefficient = self.get_number(0, term)
				coefficient = if_assign(coefficient is '', '1', coefficient)
				coefficient = if_assign(coefficient is '-', '-1', coefficient)
				coefficients.append(coefficient)
		return coefficients

	@staticmethod
	def beautify(expression):
		"""Beautifies a mathematical expression, turning '--' into '+',
		'+*' into '*', etc."""

		if '--' in expression:
			expression = expression.replace('--', '+')

		if '*+' in expression:
			expression = expression.replace('*+', '*')

		if expression[0] == '+':
			expression = expression.replace('+', '', 1)

		if '+-' in expression:
			expression = expression.replace('+-', '-')

		if '=+' in expression:
			expression = expression.replace('=+', '=')

		expression = expression.replace('/+', '/')

		return expression


EXPR = Expression("22x*5x-92 = -42x")
SECOND = Expression("1/2x + 6 - 2y = 4")

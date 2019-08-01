"""Base class for algebraic operations."""

from misc import if_assign, num, isanumber
from exc import NonAlgebraicOperationError, InvalidOperationError
from expression import Expression

class TermOperations:
    """Defines operations between algebraic terms.
    This class is not ment to have instances, but is a placeholder
    for static methods to be used on terms constructed on classes
    deriving from Expression (see expression.py)."""

    @staticmethod
    def ispowered(a):
        """Returns true if a is being elevated by an exponent."""

        return True if '**' in a else False

    @staticmethod
    def getpower(a):
        """Returns exponent of term a."""

        if TermOperations.ispowered(a):
            return num(a[a.find('**') + 2:])
        elif isanumber(a):
            return 0
        return 1

    @staticmethod
    def starts_with_minus(a):
        """True if a is negative, false otherwise."""

        if a.count('-') != 0 and a.count('-') % 2 != 0:
            return True
        return False

    @staticmethod
    def commonvars(a, b):

        a, b = Expression(a, no_vars_intended=True), Expression(b, no_vars_intended=True)
        common_vars = []

        for var in a.variables:
            if var in b.variables:
                common_vars.append(var)

        return common_vars

    @staticmethod
    def add(a, b, non_algebraic=False):
        """Returns the expression resultant of adding terms a and b."""

        a = Expression(a, no_vars_intended=True)
        b = Expression(b, no_vars_intended=True)

        if isanumber(a.expression) or isanumber(b.expression):

            if non_algebraic is True:
                return num(num(a.expression) + num(b.expression))
            raise NonAlgebraicOperationError

        if len(a.terms) > 1 or len(b.terms) > 1:
            raise InvalidOperationError(a, b)

        if TermOperations.getpower(a.expression) is not TermOperations.getpower(b.expression) or a.variables != b.variables:
            operator = if_assign(b.expression.startswith('-'), '', '+')
            return Expression.beautify(a.expression + operator + b.expression)

        a_coefficient = a.get_number(0)
        b_coefficient = b.get_number(0)

        result = str(num(a_coefficient) + num(b_coefficient))
        result = if_assign(result == '1', "", result)
        result = if_assign(result == '-1', "-", result)

        result += "".join(a.variables) + '**' + str(TermOperations.getpower(a.expression))
        if result.endswith('**1'):
            result = result.replace('**1', '')
        return Expression.beautify(result)

    @staticmethod
    def substract(a, b):
        """Returns the expression resultant of substracting terms a and b."""

        a = Expression(a, no_vars_intended=True)
        b = Expression(b, no_vars_intended=True)

        if isanumber(a.expression) or isanumber(b.expression):
            raise NonAlgebraicOperationError

        if len(a.terms) > 1 or len(b.terms) > 1:
            raise InvalidOperationError(a, b)

        if TermOperations.getpower(a.expression) is not TermOperations.getpower(b.expression) or a.variables != b.variables:
            result = a.expression + '-' + b.expression
            return Expression.beautify(result)

        a_coefficient = a.get_number(0, frac_to_number=True)
        b_coefficient = b.get_number(0, frac_to_number=True)

        result = str(num(a_coefficient) - num(b_coefficient))
        result = if_assign(result == '1', "", result)
        result = if_assign(result == '-1', "-", result)

        result += "".join(a.variables) + '**' + str(TermOperations.getpower(a.expression))
        return Expression.beautify(result)

    @staticmethod
    def multiply(a, b):
        """Multiplies terms a and b."""

        a = Expression(a, no_vars_intended=True)
        b = Expression(b, no_vars_intended=True)

        print("P of A : ", TermOperations.getpower(a.expression))
        print("P of B : ", TermOperations.getpower(b.expression))

        power = str(if_assign(TermOperations.getpower(a.expression) >= TermOperations.getpower(b.expression), TermOperations.getpower(a.expression), TermOperations.getpower(b.expression)))
        variables = set(a.variables + b.variables)

        if len(TermOperations.commonvars(a.expression, b.expression)) > 0:
            power = str(int(TermOperations.getpower(a.expression)) + int(TermOperations.getpower(b.expression)))

        power = if_assign(power == '1', '', power)

        if power == '1':
            return "".join(variables)

        a_coefficient = a.get_number(0)
        b_coefficient = b.get_number(0)

        print("POWER IS ,", power)

        result = str(int(a_coefficient) * int(b_coefficient)) + "".join(variables) + '**' + power
        return Expression.beautify(result)

    @staticmethod
    def divide(a, b):
        a = Expression(a)
        b = Expression(b)

        variables = set(a.variables + b.variables)
        power = '**' + str(int(TermOperations.getpower(a.expression)) - int(TermOperations.getpower(b.expression)))
        power = if_assign(power == '**1', '', power)

        if power == '**0':
            return "/".join(variables)

        a_coefficient = a.get_number(0)
        b_coefficient = b.get_number(0)

        result = str(num(int(a_coefficient) / int(b_coefficient))) + "/".join(variables)
        result = if_assign(power != '', '(' + result + ')' + power, result)
        return Expression.beautify(result)


A = "-5x"
B = "4x"


#A = "-9z**2"
#B = "3x**5"
#print("TERMS ARE ", A, " ", B)
#print(TermOperations.getpower(A))
#print(TermOperations.multiply(A, B))

# Find a way to individualize powers, so that we are not talking about the exponents of a whole term, but of the elements of that term.


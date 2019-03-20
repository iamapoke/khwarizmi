import math
from equations import Equation
from polynomials import Polynomial
from expression import Expression
from exc import NoSquareError
from enum import Enum, auto
from misc import num
from matplotlib import pyplot as plt

class RootTypes(Enum):

    DistinctRealRoots = "Distinct real roots"
    IdenticRealRoots = "Identical real roots"
    ComplexConjugateRoots = "Complex conjugate roots"

class Quadratic(Polynomial):

    def __init__(self, polynomial):
        Polynomial.__init__(self, polynomial)
        self._complete()
        self.discriminant = self.get_discriminant()
        self._roots_type = self.get_roots_type()
        self.roots = self.get_roots()
        self.vertex = self.get_vertex()
        self.axis_of_simmetry = 'x = ' + str(self.vertex[0])

    def _complete(self):
        if not any('**2' in term for term in self.terms):
            raise NoSquareError(self.expression)

        term_count = len(self.terms)

        if term_count is 3:
            return

        if term_count is 2:
            if any(self.variables[0] not in term for term in self.terms):
                self.terms.insert(1, '0' + self.variables[0])
            else:
                self.terms.insert(2, '0')

        if term_count is 1:
            self.terms.insert(1, '0' + self.variables[0])
            self.terms.insert(2, '0')

        self.expression = Expression.beautify('+'.join(self.terms))

    def getabc(self):
        """Returns values of a, b and c coefficients from standard quadratic form,
        ax**2 + bx + c"""
        return self.get_number(0, self.terms[0]), self.get_number(0, self.terms[1]), self.terms[2]

    def get_discriminant(self):
        """Returns the discriminant an evaluated number; this means it will not return the discriminants
        form but its already simplified value."""

        a, b, c = self.getabc()

        disc = '(' + b + ")**2-4*" + a + "*" + c
        return eval(disc)

    def get_roots_type(self):
        """Returns a string defining this quadratic's roots
        nature; i.e, is it complex, real, distinct or identic."""

        if self.discriminant > 0:
            return RootTypes.DistinctRealRoots
        if self.discriminant == 0:
            return RootTypes.IdenticRealRoots
        return RootTypes.ComplexConjugateRoots

    @property
    def isascendant(self):
        return False if self.getabc()[0].startswith('-') else True

    def bhaskarize(self):
        """Returns a string representation of this quadratic under Bhaskara's
        formula."""

        disc = str(self.discriminant)
        a, b, c = self.getabc()
        den = eval("2*" + a)

        bhask = ''

        if self._roots_type == RootTypes.ComplexConjugateRoots:
            if disc.startswith('-'):
                disc = disc.replace('-', '')

        bhask = '(-' + b + ' +/- i(' + disc +'**½)) / ' + str(den)
        if self._roots_type != RootTypes.ComplexConjugateRoots:
            bhask = bhask.replace('i', '')
        return bhask

    def get_roots(self):
        """Returns the roots of this quadratic.
        Depending on the case, it'll return an int, a string or
        a tuple of two integers. Unfortunately, this can't be
        solved in an elegant way, and is a consequence of the different
        possible results of solving for roots.
        User should be careful before manipulating roots because of this,
        but can help himself using the roots_type attribute to know what
        to expect from the roots."""

        if self._roots_type == RootTypes.ComplexConjugateRoots:
            return [self.bhaskarize()]

        bhask = self.bhaskarize().replace('½', '0.5')

        if self._roots_type == RootTypes.IdenticRealRoots:
            return num(eval(bhask.replace('+/-', '+')))

        roots = []
        roots.append(eval(bhask.replace('+/-', '+')))
        roots.append(eval(bhask.replace('+/-', '-')))

        return roots

    def get_vertex (self):
        """Returns this quadratic's vertex (point intersected by
        axis of symmetry)."""

        a, b, c = self.getabc()

        x = eval('-' + b + '/(2*'+ a + ')')
        y = self.evaluate(x)

        return (num(x), num(y))

    def graph (self, domain_range, axis_range=15):
        """Graphs this quadratic from x1 = -domain_range
        and x2 = domain_range.
        Draws x and y axis with the same logic using axis_range."""

        x_coors, y_coors = [], []

        for x in range(-domain_range, domain_range + 1):
            x_coors.append(x)
            y_coors.append(self.evaluate(x))


        y_axis, x_axis = [max(float(s) for s in y_coors)*1.5, min(float(s) for s in y_coors)], [-axis_range, axis_range]
        plt.plot(x_axis, [0]*len(x_axis), 'go-')
        plt.plot(s_axis_x, s_axis_y)
        plt.plot([0]*len(y_axis), y_axis, 'go-')

        plt.plot(x_coors, y_coors)
        plt.show()

    @property
    def roots_type(self):
        return self._roots_type.value


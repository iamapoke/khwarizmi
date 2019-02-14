import math

from equations import Equation
from polynomials import Polynomial
from exc import NegativeSquareError
from enum import Enum, auto
from misc import num
from matplotlib import pyplot as plt

class RootTypes(Enum):

    DistinctRealRoots = auto()
    IdenticRealRoots = auto()
    ComplexConjugateRoots = auto()


class Quadratic(Polynomial):

    def __init__(self, polynomial):
        Polynomial.__init__(self, polynomial)
        self.discriminant = self.get_discriminant()
        self._root_type = None
        self.roots_nature = self.get_roots_nature()
        self.roots = self.get_roots()

    def getabc(self):
        """Returns a tuple containing the values of a, b and c variables of Bhaskara's formula"""
        return (self.get_number(0, self.terms[0]), self.get_number(0, self.terms[1]), self.terms[2])

    def get_discriminant(self):
        """Returns the discriminant an evaluated number; this means it will not return the discriminants
        form but its already simplified value."""

        abc = self.getabc()
        a, b, c = abc[0], abc[1], abc[2]

        disc = b + "**2-4*" + a + "*" + c
        return eval(disc)

    def get_roots_nature(self):
        """Returns a string defining this quadratic's roots
        nature; i.e, is it complex, real, distinct or identic."""

        if self.discriminant > 0:
            self._root_type = RootTypes.DistinctRealRoots
            return 'Two real distinct roots'
        if self.discriminant == 0:
            self._root_type = RootTypes.IdenticRealRoots
            return 'Two undistinct real roots'
        self._root_type = RootTypes.ComplexConjugateRoots
        return 'Two complex conjugate roots'

    def bhaskarize(self):
        """Returns a string representation of this quadratic under Bhaskara's
        formula."""

        disc = self.discriminant
        abc = self.getabc()
        a, b, c = abc[0], abc [1], abc [2]
        den = eval("2*" + a)

        bhask = ''

        bhask = '(-' + b + ' +/- i(' + str(disc) +')**½) /' + str(den)
        if self._root_type != RootTypes.ComplexConjugateRoots:
            bhask = bhask.replace('i', '')
        return bhask

    def get_roots(self):
        """Returns a string representation of this quadatric's roots.
        It returns a string because complex roots can't be integers/floats,
        since Python can't evaluate them, and every function should return
        a single value type."""

        if self._root_type == RootTypes.ComplexConjugateRoots:
            return self.bhaskarize()

        bhask = self.bhaskarize().replace('½', '0.5')

        if self._root_type == RootTypes.IdenticRealRoots:
            return eval(bhask.replace('+/-', '+'))

        roots = []
        roots.append(str(eval(bhask.replace('+/-', '+'))))
        roots.append(str(eval(bhask.replace('+/-', '-'))))

        return roots

    def graph (self, domain_range, axis_range=15):
        """Graphs this quadratic from x1 = -domain_range
        and x2 = domain_range.
        Draws x and y axis with the same logic using axis_range."""

        x_coors, y_coors = [], []

        for x in range(-domain_range, domain_range + 1):
            x_coors.append(x)
            y_coors.append(self.evaluate(x))


        y_axis, x_axis = [axis_range, min(float(s) for s in y_coors)], [-axis_range, axis_range]

        plt.plot(x_axis, [0]*len(x_axis), 'go-')
        plt.plot([0]*len(y_axis), y_axis, 'go-')

        plt.plot(x_coors, y_coors)
        plt.show()


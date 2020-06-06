# http://reports-archive.adm.cs.cmu.edu/anon/1995/CMU-CS-95-113.pdf

from metaL import *

# naive Rete algorithm implementation
class Rete(Object):
    pass


# p.21

class Working(Rete):
    pass
class Production(Rete):
    pass


wm = Working('memory')
pm = Production('memory')


B1 = Symbol('B1')
B2 = Symbol('B2')
B3 = Symbol('B3')
B4 = Symbol('B4')
on = Op('on')
leftof = Op('left-of')
color = Op('color')
red = Color('red')
blue = Color('blue')
table = Symbol('table')

class Triplet(Rete, Vector):

    def __init__(self, X, Y, Z):
        Vector.__init__(self, '')
        self // X // Y // Z

    def dump(self, depth, prefix):
        return self.pad(depth) + prefix + \
            '( %s ^%s %s )' % (
                self.nest[0]._val(), self.nest[1]._val(), self.nest[2]._val())


# (identifier ^attribute value)

wm[1] = Triplet(B1, on, B2)
wm[2] = Triplet(B1, on, B3)
wm[3] = Triplet(B1, color, red)
wm[4] = Triplet(B2, on, table)
wm[5] = Triplet(B2, leftof, B3)
wm[6] = Triplet(B2, color, blue)
wm[7] = Triplet(B3, leftof, B4)
wm[8] = Triplet(B3, on, table)
wm[9] = Triplet(B3, color, red)
print(wm)

# p.22 triplets

class Rule(Rete, Vector):
    def __init__(self, LHS, RHS=False):
        Vector.__init__(self, '')
        self['LHS'] = LHS
        if RHS:
            self['RHS'] = RHS

class Var(Rete, Symbol):
    def _val(self): return '?%s' % self.val


x = Var('x')
y = Var('y')
z = Var('z')

pm // Rule(
    Vector('')
    // Triplet(x, on, y)
    // Triplet(y, leftof, z)
    // Triplet(z, color, red)
)
print(pm)

# p.23

class Alpha(Rete): pass

am = Alpha('memory')

print(am)

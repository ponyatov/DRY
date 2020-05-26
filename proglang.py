from metaL import *

hello = Object('Hello') // Object('World')
hello << Object('left') ; hello >> Object('right')
print(hello)


class Instruction(Object): pass
class World(Object): pass
w = World('')
ins1 = Instruction(1) ; w // ins1
ins2 = Instruction(2) ; w // ins2 ; ins2['dep'] = ins1
ins3 = Instruction(3) ; w // ins3 ; ins3['dep'] = ins1
print(w)


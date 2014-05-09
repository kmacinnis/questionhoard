from sympy import *
from math import copysign





posneg = [S(1),S(-1)]
one_digit_primes = [S(2),S(3),S(5),S(7)]
small_two_digit_primes = [S(11),S(13),S(17),S(19)]
two_digit_primes = [S(i) for i in (11,13,17,19,23,29,31,
                                   37,41,43,47,53,59,61,
                                   67,71,73,79,83,89,97)]
ln = function.Function('ln')
prettyfractions = [Rational(*i) for i in 
    [(1,2),(1,3),(2,3),(1,4),(3,4),(1,5),(2,5),(3,5),(4,5)]]
pythagorean_triples = [(S(i[0]),S(i[1]),S(i[2])) for i in
        [(3,4,5), (5,12,13), (7,24,25), (8,15,17), (9,40,41), 
        (11,60,61), (12,35,37), (13,84,85), (16,63,65),
        (20,21,29), (28,45,53), (28,45,53), (36,77,85)]]
unitcirclefractions = flatten([(i,-i) for i in [sqrt(i)/2 for i in (1,2,3)]])

def plus_minus(s):
    return sorted(set(flatten([(i,-i) for i in s])))

def integers_between(a,b):
    a,b = sorted([int(a), int(b)])
    return [S(i+a) for i in range(b-a+1)]

def is_rel_prime(*args):
    return gcd(*args) == 1

def has_duplicates(*args):
    return len(args) != len(set(args))

def round(x, d=0):
    p = 10**d
    return floor((x * p) + copysign(0.5, x))/p


import random
from math import atan2, cos, pi, sin, sqrt
from numpy import logspace
import matplotlib.pyplot as plt
from typing import *

# This is a puzzle from The Fiddler. See https://thefiddler.substack.com/p/a-pi-day-puzzle

# I am going to assume a radius of 1 for the island. The distance from the diametric beach is
# simply the `y` coordinate in a Cartesian system. The distance from the semicircular beach is
# 1 - r in a polar system.

Point = Tuple[int, int] # A point is an (x, y) coordinate in a Cartesian system or a (r, theta) in a polar system.

def monte_carlo(N: int) -> float:
    """Perform a Monte Carlo search of random points on a semicircular "island"
    and determine the probability of a point being closer to the "Diametric Beach" or
    the "Semicircular Beach". I am going to assume an island of radius 1. `N` is the
    number of points to use to estimate the probability."""
    cart = generatePointsCart(N, 1.0)
    distanceFromDiam = [p[1] for p in cart]
    polar = [cartesian2polar(p) for p in cart]
    distanceFromSemi = [1.0 - p[0] for p in polar]
    return sum([1 for (dSemi, dDiam) in zip(distanceFromSemi, distanceFromDiam) if dDiam < dSemi]) / len(cart)

# This function below was originally used, but the distribution is incorrect for a Monte Carlo method.
# Create plots of N=1000 to see the funky distribution.
def generatePointsPolar(N: int, r=1.0) -> List[Point]:
    """Return a list of points in a polar coordinate system that are uniformly distributed on
    a semicircle. `r` is the radius of the semicircle."""
    return list(zip([random.uniform(0.0, r) for _ in range(N)],
                [random.uniform(0.0, pi) for _ in range(N)]))

def generatePointsCart(N: int, r=1.0) -> List[Point]:
    """Return a list of points in a cartesian coordinate system that are uniformly distributed on
    a semicircle. `r` is the radius of the semicircle."""
    points = list(zip([random.uniform(-r, r) for _ in range(N)],
                      [random.uniform(0.0, r) for _ in range(N)]))
    return [p for p in points if cartesian2polar(p)[0] <= r]

def polar2cartesian(p: Point) -> Point:
    """Convert a polar (r, theta) coordinate to a Cartesian (x, y) coordinate."""
    (r, theta) = p
    return (r*cos(theta), r*sin(theta))

def cartesian2polar(p: Point) -> Point:
    """Convert a cartesian (x, y) coordinate to a polar (r, theta) coordinate."""
    (x, y) = p
    return (sqrt(x**2 + y**2), atan2(y, x))

def do(N: int=6):
    """Perform `N` Monte Carlo simulations in a logarithmic space and compare results."""
    print('Estimated probabilty of being closer to the "Diametric Beach":')
    for n in logspace(1, N, num=N, dtype=int):
        p = monte_carlo(n)
        print(f'Number of samples: {n:7} | Probability: {p:6.4f}')



#monte_carlo(10000)
do()

print('')
print("""The mathematical solution was derived by finding the function where the distance to the
Diameter Beach is equal to the distance from the Semicircular Beach. Then to get the probabilty
we need to calculate the area under that function and divide it by the area of the semicircle.
The distance from the Diameter Beach is y, the distance from the Semicircular Beach is 1 - r,
assuming a semicircle of radius 1.
Therfore we have y = 1 - r where r = sqrt(x**2 + y**2).
Solving for y gives y = (1 - x**2)/2. Integrating y from -1 to 1 gives 2/3.
The area of the semicircle is pi*r**2/2 = pi/2. Therefore, the probability is (2/3)/(pi/2).""")
print('')
print(f'(2/3/(pi/2) = {(2/3)/(pi/2):6.4f}')


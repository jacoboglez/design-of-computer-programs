import itertools
from time import perf_counter


"""
 Zebra Puzzle

1 There are five houses.
2 The Englishman lives in the red house.
3 The Spaniard owns the dog.
4 Coffee is drunk in the green house.
5 The Ukrainian drinks tea.
6 The green house is immediately to the right of the ivory house.
7 The Old Gold smoker owns snails.
8 Kools are smoked in the yellow house.
9 Milk is drunk in the middle house.
10 The Norwegian lives in the first house.
11 The man who smokes Chesterfields lives in the house next to the man with the fox.
12 Kools are smoked in a house next to the house where the horse is kept.
13 The Lucky Strike smoker drinks orange juice.
14 The Japanese smokes Parliaments.
15 The Norwegian lives next to the blue house.

Who drinks water? Who owns the zebra? 
"""


def zebra_puzzle():
    "Return a tuple (WATER, ZEBRA) indicating their house numbers."
    houses = [first, _, middle, _, _] = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(houses))

    return next( (WATER, ZEBRA)
            for (red, green, ivory, yellow, blue) in c(orderings)
            if imright(green, ivory)        # 6
            for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in c(orderings)
            if Englishman is red            # 2
            if Norwegian is first           # 10
            if nextto(Norwegian, blue)      # 15
            for (coffee, tea, milk, oj, WATER) in c(orderings)
            if coffee is green              # 4
            if Ukranian is tea              # 5
            if milk is middle               # 9
            for (OldGold, Kools, Chesterfields, Lucky, Parliaments) in c(orderings)
            if Kools is yellow              # 8
            if Lucky is oj                  # 13
            if Japanese is Parliaments      # 14
            for (dog, snails, fox, horse, ZEBRA) in c(orderings)
            if Spaniard is dog              # 3
            if OldGold is snails            # 7
            if nextto(Chesterfields, fox)   # 11
            if nextto(Kools, horse)         # 12            
            )


def zebra_puzzle_slow():
    "Return a tuple (WATER, ZEBRA) indicating their house numbers."
    houses = [first, _, middle, _, _] = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(houses))

    return next( (WATER, ZEBRA)
            for (red, green, ivory, yellow, blue) in orderings
            for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in orderings
            for (coffee, tea, milk, oj, WATER) in orderings
            for (OldGold, Kools, Chesterfields, Lucky, Parliaments) in orderings
            for (dog, snails, fox, horse, ZEBRA) in orderings
            if Englishman is red            # 2
            if Spaniard is dog              # 3
            if coffee is green              # 4
            if Ukranian is tea              # 5
            if imright(green, ivory)        # 6
            if OldGold is snails            # 7
            if Kools is yellow              # 8
            if milk is middle               # 9
            if Norwegian is first           # 10
            if nextto(Chesterfields, fox)   # 11
            if nextto(Kools, horse)         # 12            
            if Lucky is oj                  # 13
            if Japanese is Parliaments      # 14
            if nextto(Norwegian, blue)      # 15
            )


def imright(a, b):
    "House h1 is immediately right of h2 if h1-h2 == 1."
    return a - b == 1


def nextto(a, b):
    "Two houses are next to each other if they differ by 1."
    return abs(a - b) == 1


# Timers

def timedcall(fn, *args, **kwargs):
    "Call function with args; return the time in seconds and result."
    t0 = perf_counter()
    result = fn(*args, **kwargs)
    t1 = perf_counter()
    return t1-t0, result


def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers)) 


def timedcalls(n, fn, *args, **kwargs):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    times = []
    if isinstance(n, int):
        for _ in range(n):
            times.append( timedcall(fn, *args, **kwargs)[0] )
    else:
        while sum(times) < n:
            times.append( timedcall(fn, *args, **kwargs)[0] )
    
    return min(times), average(times), max(times)


# Generator functions

def all_ints():
    "Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ..."
    N = 0
    yield N
    while True:
        N += 1
        yield N
        yield -N


def instument_fn(fn, *args, **kwargs):
    """Count the number of times the sequences instrumented with c(sequences)
    and its items are iterated."""
    c.starts, c.items = 0, 0
    result = fn(*args, **kwargs)
    print(f'{fn.__name__} got {result} with {c.starts} iters over {c.items} times.')
    return result


def c(sequence):
    """Generate items in a sequence; keeping counts as we go. c.starts is the 
    number of sequences started; c.items is the number of items generated."""
    # Initialize c.starts and c.items to avoid AttributeError
    if not hasattr(c, 'starts'): c.starts = 0
    if not hasattr(c, 'items'): c.items = 0

    c.starts += 1
    for item in sequence:
        c.items += 1
        yield item


if __name__ == "__main__":

    print('Solution to the zebra puzzle:')
    WATER, ZEBRA = zebra_puzzle()
    print(f'{WATER=}')
    print(f'{ZEBRA=}')
    print()

    a = perf_counter()
    min_time, avg_time, max_time = timedcalls(1.0, zebra_puzzle)
    b = perf_counter()
    print(f'The execution time was on average: {avg_time:.5f}s (min={min_time:.5f}s, max={max_time:.5f}s).')
    print()

    instument_fn(zebra_puzzle)

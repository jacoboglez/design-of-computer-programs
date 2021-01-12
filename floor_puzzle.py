"""
Hopper, Kay, Liskov, Perlis, and Ritchie live on 
different floors of a five-floor apartment building. 

1 Hopper does not live on the top floor. 
2 Kay does not live on the bottom floor. 
3 Liskov does not live on either the top or the bottom floor. 
4 Perlis lives on a higher floor than does Kay. 
5 Ritchie does not live on a floor adjacent to Liskov's. 
6 Liskov does not live on a floor adjacent to Kay's. 

Where does everyone live?  
"""

import itertools


def floor_puzzle():
    "Solve the puzzle."
    floors = [bottom, _, _, _, top] = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(floors))

    for Hopper, Kay, Liskov, Perlis, Ritchie in orderings:
        if all([
            Hopper != top,                              # 1
            Kay != bottom,                              # 2
            (Liskov != top) and (Liskov != bottom),     # 3
            Perlis > Kay,                               # 4
            not adjacent(Ritchie, Liskov),              # 5
            not adjacent(Liskov, Kay),                  # 6
            ]):
                return [Hopper, Kay, Liskov, Perlis, Ritchie]


def adjacent(a, b):
    "Return true if floors a and b are adjacent."
    return abs(a-b) == 1


if __name__ == "__main__":
    names = 'Hopper Kay Liskov Perlis Ritchie'.split()
    print("Name      Floor")
    for name, floor in zip(names, floor_puzzle()):
        print(f'{name:<9} {floor}')

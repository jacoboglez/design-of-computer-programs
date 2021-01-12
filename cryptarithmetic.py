import re
import itertools
from zebra import timedcall
import time
import warnings


"""
Module that solves cryptarithmetic puzzles such as:

Obtain the number that corresponds with each letter so the following is true
  ODD
+ ODD
------
 EVEN

"""

EXAMPLES = """TWO + TWO == FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < TRHEE
RAMN == R**3 + RM**3 == N**3 + RX**3
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANETS])""".splitlines()


def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    for digits in itertools.permutations(range(10), len(letters)):
        try:
            if f(*digits) is True:
                table = str.maketrans(letters, ''.join(map(str, digits)))
                yield formula.translate(table)
        except ArithmeticError:
            pass      


def compile_formula(formula):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as params of function. The first digit of a multi-digit
    number can't be 0. For example, 'YOU == ME**2 returns
    (lambda Y, M, E, U, O: (U+10*O+100*Y) == (E+10*M)**2), 'YMEUO' """  
    letters = ''.join( set(c for c in formula if c.isupper()) )
    params = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    
    # Check for leading 0
    firstletters = set(re.findall(r'\b([A-Z])[A-Z]', formula))
    if firstletters:
        tests = ' and '.join(L+'!=0' for L in firstletters)
        body = f'{tests} and ({body})'
    
    f = f'lambda {params}: {body}'
    return eval(f), letters


def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if word.isupper():
        compiled_word = '+'.join( [f'{10**i}*{c}' for i, c in enumerate(word[::-1])] )
        return '(' + compiled_word + ')'
    else:
        return word


def solve_slow(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            yield f


def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join( set(c for c in formula if c.isupper()) )
    for digits in itertools.permutations('1234567890', len(letters)):
        table = str.maketrans(letters, ''.join(digits))
        yield formula.translate(table)


def valid(f):
    "Formula f is valid iff it has no numbers with leading zero and evals true."
    if len(f) > len(f.lstrip('0')): return False
    with warnings.catch_warnings(): 
        # Avoid a syntax warning:
        #   SyntaxWarning: "is not" with a literal. Did you mean "!="?
        warnings.simplefilter("ignore")
        try:
            return not re.search(r'\b0[0-9]', f) and eval(f)
        except ArithmeticError:
            return False


def test():
    # Test function valid
    assert valid('030 == 30') == False
    assert valid('30 == 030') == False
    assert valid('1 + 2 + 27 == 30') == True

    # Test function compile_word
    assert compile_word('YOU') == '(1*U+10*O+100*Y)'
    assert compile_word('AA') == '(1*A+10*A)'

    # Test function compile_formula
    f, letters = compile_formula('A + B == BA')
    if letters == 'AB':
        assert f(1,0) == False
    else:
        assert f(0, 1) == False

    # Test some solutions
    assert next(solve("X / X == X")) == "1 / 1 == 1"
    assert next(solve("sum(range(AA)) == BB")) == "sum(range(11)) == 55"
    assert next(solve("RAMN == R**3 + RM**3 == N**3 + RX**3")) == "1729 == 1**3 + 12**3 == 9**3 + 10**3"


def solve_examples(n=1):
    """Return the n first solutions to each of the EXAMPLES."""
    tic = time.perf_counter()
    for example in EXAMPLES:
        print()
        print(11*' ', example)
        tic2 = time.perf_counter()
        for sol in itertools.islice(solve(example), n):
            print(f'{time.perf_counter()-tic2:6.4f}s:    {sol}')
    toc = time.perf_counter()
    print(f'{toc-tic:6.4f}s total.')


test()

if __name__ == "__main__":
    solve_examples(3)
    
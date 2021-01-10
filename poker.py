import random
from time import time
import itertools

DECK = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 
HAND_NAMES = [
    "High Card",
    "Pair",
    "2 Pair",
    "3 Kind",
    "Straight",
    "Flush",
    "Full House",
    "4 Kind",
    "Straight Flush"]
EXPECTED_PERC = [50.11, 42.25, 4.75, 2.11, 0.39, 0.196, 0.140, 0.024, 0.0015]


def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    hands = []
    if '?B' in hand:
        hand.remove('?B')
        for card in [r+s for r in '23456789TJQKA' for s in 'SC']:
            if card not in hand:
                hands.append([*hand, card])
    else:
        hands.append(hand)
    final_hands = []
    if '?R' in hand:
        for h in hands:
            h.remove('?R')
            for card in [r+s for r in '23456789TJQKA' for s in 'HD']:
                if card not in h:
                    final_hands.append([*h, card])
    else:
        final_hands = hands

    return best_hand( max(final_hands, key=best_hand) )


def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    hands = itertools.combinations(hand, 5)
    return list( max(hands, key=hand_rank) )


def deal(numhands, n=5, deck=DECK.copy()):
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]


def poker(hands):
    "Return the best hand: poker([hand, ...]) => hand"
    return allmax(hands, key=hand_rank)


def allmax(iterable, key=lambda x: x):
    "Return a list of all items equal to the max of the iterable."
    maxval = key(max(iterable, key=key))
    allmaxes = [i for i in iterable if key(i)==maxval]
    return allmaxes


def hand_rank(hand):
    "Return a value indicating the rank of a certain hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks): # Double pairs
        return (2, *two_pair(ranks), kind(1, ranks)) 
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks) 


def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = sorted(['--23456789TJQKA'.index(r) for r,s in hand], reverse=True)
    if ranks == [14, 5,4,3,2]: # Ace-Low Straight case
        return [5,4,3,2,1]
    return ranks


def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return ranks == list(range(ranks[0], ranks[-1]-1, -1))


def flush(hand):
    "Return True if all the cards have the same suit."
    suits = set([s for r,s in hand])
    return len(suits) == 1


def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None


def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    pairs = [r for r in set(ranks) if ranks.count(r)==2]
    if len(pairs) == 2:
        return tuple(sorted(pairs, reverse=True))
    else:
        return None


def test():
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full Hous
    tp = "5S 5D 9H 9C 6S".split() # Two pairs
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight

    # Test function card_ranks
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    # Test function straight
    assert straight(card_ranks(sf)) == True
    assert straight(card_ranks(fk)) == False
    assert straight(card_ranks(fh)) == False
    assert straight(card_ranks(al)) == True 

    # Test function flush
    assert flush(sf) == True
    assert flush(fk) == False
    assert flush(fh) == False
    assert flush(tp) == False

    # Test function kind
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7

    # Test function two_pair
    assert two_pair(fkranks) == None
    assert two_pair(tpranks) == (9, 5)

    # Test function hand_rank
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    assert hand_rank(tp) == (2, 9, 5, 6)

    assert hand_rank("JC TC 9C 8C 7C".split()) == (8, 11)
    assert hand_rank("AS AH AD AC QH".split()) == (7, 14, 12)
    assert hand_rank("8S 8H 8D KS KC".split()) == (6, 8, 13)
    assert hand_rank("TD 8D 7D 5D 3D".split()) == (5, [10, 8, 7, 5, 3])
    assert hand_rank("JC TS 9D 8C 7C".split()) == (4, 11)
    assert hand_rank("7H 7D 7C 5C 2C".split()) == (3, 7, [7, 7, 7, 5, 2])
    assert hand_rank("JD JC 3S 3H KH".split()) == (2, 11, 3, 13)
    assert hand_rank("2H 2S JD 6H 3C".split()) == (1, 2, [11, 6, 3, 2, 2])
    assert hand_rank("7C 5C 4C 3C 2D".split()) == (0, [7, 5, 4, 3, 2]) 

    # Test function poker
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf, sf2, fk, fh]) == [sf, sf2]

    # Test best_hands
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])

    # Test best_wild_hand
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    

def hand_percentages(n=100_000):
    "Sample n random hands and print a table of percentages for each type of hand."
    counts = [0]*9
    for i in range(n//10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    
    print('Hand percentages:')
    print('')
    print('Hand             Measured  Expected')
    print('-----------------------------------')
    for i in reversed(range(9)):
        print(f'{HAND_NAMES[i]:>14}: {100*counts[i]/n:6.3f} %   {EXPECTED_PERC[i]:6.3f} %')


test()

if __name__ == "__main__":
    # hand_percentages(n=100_000)
    pass

"""
Q1
helped by:
https://bobbyhadz.com/blog/python-find-index-of-first-element-greater-than
https://stackoverflow.com/questions/374626/how-can-i-find-all-the-subsets-of-a-set-with-exactly-n-elements
https://stackoverflow.com/questions/52775382/attributeerror-generator-object-has-no-attribute-sort

"""
# from functools import lru_cache
import numpy as np
import itertools
import doctest


def bounded_subsets(lst: list, sm):
    """
    >>> for s in bounded_subsets([1,2,3], 4):
    ...     print(s, end="")
    [][1][2][3][1, 2][1, 3]
    >>> for s in bounded_subsets(range(50, 150), 103):
    ...     print(s, end="")
    [][50][51][52][53][54][55][56][57][58][59][60][61][62][63][64][65][66][67][68][69][70][71][72][73][74][75][76][77][78][79][80][81][82][83][84][85][86][87][88][89][90][91][92][93][94][95][96][97][98][99][100][101][102][103][50, 51][50, 52][50, 53][51, 52]
    >>> for s in zip(range(5), bounded_subsets(range(100), 1000000000000)):
    ...     print(s, end="")
    (0, [])(1, [0])(2, [1])(3, [2])(4, [3])
    >>> for s in bounded_subsets([1,2,3,4,5,6], 7):
    ...     print(s, end="")
    [][1][2][3][4][5][6][1, 2][1, 3][1, 4][1, 5][1, 6][2, 3][2, 4][2, 5][3, 4][1, 2, 3][1, 2, 4]
    """
    # check if input is valid
    if not all(isinstance(e, (int, float)) for e in lst) or not (isinstance(sm, (int, float))):
        raise Exception("not all input are numbers")

    # chack for base cases
    if sm < 0 or len(lst) == 0:
        yield []
        return

    # sorting the list
    lst = sorted(lst)

    # get the first index that is sum grater then the sum, it will be the last combination to check.
    last_index = next((index for index, item in enumerate(
        np.cumsum(lst)) if item > sm), None)

    if last_index is None:
        last_index = len(lst)

    cache = []  # can't use lru_cache in here
    for i in range(0, last_index + 1):
        for comb in itertools.combinations(lst, i):
            comb = list(comb)
            if comb not in cache:
                if sum(comb) <= sm:
                    cache.append(comb)
                    yield comb

def bounded_subsets_sorted(lst, sm):
    """
    >>> for s in bounded_subsets_sorted([1,2,3,4,5,6], 7):
    ...     print(s, end="")
    [][1][2][3][1, 2][4][1, 3][5][1, 4][2, 3][6][1, 5][2, 4][1, 2, 3][1, 6][2, 5][3, 4][1, 2, 4]
    >>> for s in bounded_subsets_sorted(range(50, 150), 103):
    ...     print(s, end="")
    [][50][51][52][53][54][55][56][57][58][59][60][61][62][63][64][65][66][67][68][69][70][71][72][73][74][75][76][77][78][79][80][81][82][83][84][85][86][87][88][89][90][91][92][93][94][95][96][97][98][99][100][101][50, 51][102][50, 52][103][50, 53][51, 52]
    """
    yield from sorted(bounded_subsets(lst, sm), key=sum)

doctest.testmod()

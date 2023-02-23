import time
from functools import wraps


def parametrized(dec):
    """
    allows adding parameters to decorated decorator
    dec: decorator to which parameters are added
    :return: decorator to be parametrized
    """
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def times(fn, n=10):
    """
    Run function n times and timeit.
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = None
        for i in range(n):
            res = fn(*args, **kwargs)
        print(f"x{n}: {fn.__name__}() took {(time.perf_counter() - start)} secs")
        return res

    return inner


@times(100000)
def cut(tour, subset):
    """
    This function takes in two inputs: a list called `tour` and a set called `subset`. It returns a list of lists.
    It sorts the index of the nodes in `tour` that are in `subset` and creates multiple sublists of `tour`
    based on the indices of the `subset` nodes. Finally, it returns a new list that contains each tour in
    `subtours` in reverse order if the first element of the tour is not in `subset`, otherwise the tour is
    returned as is.

    Args:
    tour: List of integers representing the nodes in a tour.
    subset: set of integers representing the nodes in a subset.

    Returns:
    List of list of integers representing the sublists of `tour`

    Restrictions:
    tour: list of integers, len(tour) > 0
    subset: set of integers, subset ⊆ tour, len(subset) > 0

    Given a list S of integers representing a tour and a subset T of S, where S = {s1, s2, ..., sn} and T = {t1,
    t2, ..., tm},
    the function cut(S, T) returns a new list of lists R, where each list in R is a sublist of S and satisfies
    the following conditions:

        For each r in R, r is a sublist of S and is either a subset of T or its complement set (S-T)
        For each r in R, if the first element of r is not in T, then r is in reverse order.
    """
    subtours, prev, last_ix = [], -1, len(tour) - 1
    for e, idx in enumerate(idxs := sorted((tour.index(node) for node in subset))):
        if e == len(idxs) - 1 and idx != last_ix:
            subtours += [tour[prev + 1: idx], tour[idx:]]
        else:
            subtours += [tour[prev + 1:idx + 1]]
            prev = idx
    return [tour if tour[0] in subset else tour[::-1] for tour in subtours if tour]


def main():
    """
    Run the cut function 10_000 times by decorating the function.
    """
    path = [780, 778, 540, 610, 414, 5, 30, 406, 596, 516, 746, 730, 512, 576, 382, 498, 374, 562, 488, 706, 708, 490, 564, 376, 500, 384, 578, 514, 740, 756, 518, 598, 408, 532, 416, 612, 542, 346, 344, 256, 294, 246, 334, 326, 238, 286, 228, 316, 318, 230, 288, 240, 328, 336, 248, 296, 258, 190, 188, 176, 178];
    subset = {416, 514, 258, 230, 542, 190}
    expected = [[514, 578, 384, 500, 376, 564, 490, 708, 706, 488, 562, 374, 498, 382, 576, 512, 730, 746, 516, 596, 406, 30, 5, 414, 610, 540, 778, 780], [416, 532, 408, 598, 518, 756, 740], [542, 612], [230, 318, 316, 228, 286, 238, 326, 334, 246, 294, 256, 344, 346], [258, 296, 248, 336, 328, 240, 288], [190, 188, 176, 178]]
    result = cut(path, subset)
    assert expected == result


if __name__ == '__main__':
    main()
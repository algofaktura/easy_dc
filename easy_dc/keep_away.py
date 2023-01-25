"""
Algorithm that takes a loop and mixes it up so that the edges are evenly distributed across the axes.

The algorithm works on both ends of the sequence alternately, with two versions of skip: head skip, and buttskip

so head, so if end: is head, if not end: butt:
"""
import random
from random import randint
from typing import List, Dict, Set, Tuple

from easy_dc.solve_np import weave_solution
from utils import get_G, id_seq, uon, count_nonturns, count_axes


zeroone = [-1, 0]


def random_sign_gen():
    while True:
        yield random.choice(zeroone)


def keep_away(A, V, loop):
    idx = loop.index(randint(0, len(A) - 1))
    loop = loop[idx:] + loop[:idx]

    def do_flip():
        end = next(switch)
        ix = loop.index(random.choice(list(A[loop[end]] - {loop[-2 if end else 1]})))
        if end:
            loop[ix + 1:] = loop[:ix:-1]
        else:
            loop[:ix] = loop[ix - 1::-1]

    switch = random_sign_gen()
    order = len(A)
    prev = len(A)
    for n in range(order // 80):
        do_flip()
        axes = count_axes(loop, V)
        if prev != axes:
            if not axes % 10:
                if prev > axes:
                    zeroone.append(-1)
                else:
                    zeroone.append(0)
                print(n, axes)
                prev = axes
    return loop


def loop_snake(s: List[int], A: Dict[int, Set[int]], V: Tuple[Tuple[int, int, int]]) -> List[int]:
    """
    flipwalk algorithm hoping to get smaller and smaller. based on ying and yang to not get caught up.

    Another technique is called "tabu search" it consist in maintaining a memory of previous solutions,
    and avoiding those solutions that have been previously visited, this aims to prevent the algorithm from getting stuck in a local minimum.

    skipped list:
    """

    def md(a: int, b: int) -> int:
        return sum([abs(V[a][i] - V[b][i]) for i in range(len(V[0]))]) // 2

    randrange = 20, 70
    lens, ct, prev = 0, 0, None
    while True:
        if s[-1] in A[s[0]]:
            return s
        elif not ct % randint(*randrange):
            s[:] = s[::-1]
        elif ct < randint(*randrange):
            ix = s.index(prev := sorted(A[s[-1]] - {s[-2], prev}, key=lambda p: md(s[s.index(p) + 1], s[0]))[-1])
            s[ix + 1:] = s[:ix:-1]
        elif ct > randint(*randrange):
            while s[-1] not in A[s[0]]:
                ix = s.index(prev := sorted(A[s[-1]] - {s[-2], prev}, key=lambda p: md(s[s.index(p) + 1], s[0]))[0])
                s[ix + 1:] = s[:ix:-1]
                ct += 1
                if A[s[-1]].difference(s) or ct > len(A) // 20 or s[-1] in A[s[0]]:
                    ct = 0
                    break
        else:
            ix = s.index(prev := (A[s[-1]] - {s[-2], prev}).pop())
            s[ix + 1:] = s[:ix:-1]
        ct = 0 if lens != len(s) else ct + 1
        lens = len(s)


def main():
    def show_turns(data):
        nonturns = count_nonturns(data, A, V)
        ax = count_axes(data, V)
        print('NONTURNS:', nonturns, '|', len(data))
        print('AXES:', ax)
    uon_range = 20800, 20800
    orders = []
    all_times = []
    for order in uon(*uon_range):
        G = get_G(order)
        A, V, VI, E, EA, W, ZA = G['A'], G['V'], G['VI'], G['E'], G['EA'], G['W'], G['ZA']
        woven = weave_solution(A, V, VI, EA, W, ZA)
        show_turns(woven)
        ax = 0
        while ax < order // 4:
            woven = keep_away(A, V, woven)
            show_turns(woven)
            woven = loop_snake(woven, A, V)
            show_turns(woven)
            print(woven)
            print(f'⭕️ {order:>7} | AX {order // 3} "🩺", {len(woven)}/{order}: {id_seq(woven, A)}')

    print(f'orders = {orders}')
    print(f'all_times = {all_times}')


if __name__ == '__main__':
    main()
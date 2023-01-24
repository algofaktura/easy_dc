"""
Algorithm that takes a loop and mixes it up so that the edges are evenly distributed across the axes.

The algorithm works on both ends of the sequence alternately, with two versions of skip: head skip, and buttskip

so head, so if end: is head, if not end: butt:
"""
from itertools import cycle
import random

from easy_dc.solve_np import weave_solution
from utils import get_G, id_seq, uon, count_nonturns, count_axes


def random_sign_gen():
    while True:
        yield random.choice([-1, 0])


def keep_away(A, V, loop):
    idx = loop.index(0)
    loop = loop[idx:] + loop[:idx]

    def do_flip():
        end = next(switch)
        ix = loop.index(random.choice(list(A[loop[end]] - {loop[-2 if end else 1]})))
        if end:
            loop[ix + 1:] = loop[:ix:-1]
        else:
            loop[:ix] = loop[ix - 1::-1]

    switch = random_sign_gen()
    axes = count_axes(loop, V)
    prev = None
    while axes < len(A) / 3:
        do_flip()
        axes = count_axes(loop, V)
        if prev != axes:
            if not axes % 10:
                print(axes)
                prev = axes
    return loop


def main():
    def show_turns(data):
        nonturns = count_nonturns(data, A, V)
        ax = count_axes(data, V)
        print('NONTURNS:', nonturns)
        print('AXES:', ax)

    uon_range = 9120, 9120
    orders = []
    all_times = []
    for order in uon(*uon_range):
        G = get_G(order)
        A, V, VI, E, EA, W, ZA = G['A'], G['V'], G['VI'], G['E'], G['EA'], G['W'], G['ZA']
        woven = weave_solution(A, V, VI, EA, W, ZA)
        print(woven)
        show_turns(woven)
        woven = keep_away(A, V, woven)
        show_turns(woven)
        print(f'⭕️ {order:>7} | "🩺", {len(woven)}/{order}: {id_seq(woven, A)}')

    print(f'orders = {orders}')
    print(f'all_times = {all_times}')


if __name__ == '__main__':
    main()
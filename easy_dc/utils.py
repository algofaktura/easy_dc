import cProfile
from datetime import datetime
from functools import wraps
from itertools import accumulate
import os
import pickle
import pstats
import time
from typing import List, Tuple

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score

from easy_dc.defs import *


_c = 0


def cp(show=False, spacing=None, label=' №', justify=0) -> int:
    """
    Increments global variable _c consecutively when called during the lifetime of executing a program regardless of scope.
    """

    def count():
        """
        Inner.
        """
        global _c
        _c += 1
        if show:
            if spacing:
                if not _c % spacing:
                    print(f"{_c}_{label}") if label else print(f"{_c}")
            else:
                out = f" {label} {_c}" if label else f"{_c}"
                print(f'{out}'.rjust(justify, ' '))
        return _c

    return count()


def uon(start=8, end=3000000, n=800) -> UonGen:
    """
    Generator for the uncentered octahedral numbers.
    """
    for i in range(n + 2):
        _uon = sum([(n * (n + 2)) for n in range(0, n * 2 + 2, 2)][:i])
        if end >= _uon >= start:
            yield _uon


def id_loop(seq: Path, A: AdjDict) -> Certificate:
    """
    Certify sequence, return sequence type broken, loop, or snake.
    """

    if any((len({*seq}) != len(A), len(seq) != len(A))):
        return "💔"
    for idx in range(len(seq)):
        if seq[idx - 1] not in A[seq[idx]]:
            return "💔"
    return '🔁'


def id_seq(seq, A, show=False) -> str or bool:
    """
    Certify sequence, return sequence type broken, loop, or snake.
    """
    for s in range(1, len(seq)):
        if seq[s - 1] not in A[seq[s]]:
            return show_broken(seq, A) if show else False
    if seq[0] in A[seq[-1]]:
        return 'loop'
    return 'snake'


def show_broken(seq, A):
    return list(filter(lambda n: not n[1], (((seq[s - 1], seq[s]), seq[s - 1] in A[seq[s]]) for s in range(len(seq)))))


def pickleload(filename, mode='rb', show=False, raise_error=False) -> Any:
    """
    Load object from a .pickle file
    """
    filename = f'{filename}.pickle' if 'pickle' not in filename else filename
    try:
        with open(filename, mode) as f:
            if show:
                print(f'🗃️ {filename}')
            try:
                return pickle.load(f)
            except pickle.UnpicklingError:
                print(filename)
    except EOFError:
        print(f"💩 {filename}")
        if raise_error:
            raise FileNotFoundError


def picklesave(to_pickle, filename, show=True, space=True) -> str:
    """
    Serialize object to .pickle file
    """
    if "pickle" not in filename:
        filename += ".pickle"
    with open(filename, 'wb') as outfile:
        pickle.dump(to_pickle, outfile, protocol=pickle.HIGHEST_PROTOCOL)
    if show:
        print(f' 💾 {filename}')
    return f'💾{" " if space else ""}{filename}'


def get_G(ORD, make=False) -> Graph:
    """
    Get DC graph.
    """
    from easy_dc.make import make_dcgraph
    if make:
        return make_dcgraph(ORD, save=True)
    try:
        if (loaded := pickleload(os.path.join(FP_GRAPHS, str(ORD)), )) is None:
            return make_dcgraph(ORD, save=True)
        return loaded
    except FileNotFoundError:
        print('GRAPH NOT IN FILE, MAKING....')
        save_G(make_dcgraph(ORD))
        return get_G(ORD)


def save_G(G):
    """
    Get DC graph.
    """
    return picklesave(G, os.path.join(FP_GRAPHS, str(len(G['A']))))


def stratify_A(A: AdjDict, V: Verts) -> GLvls:
    """
    Partition the Adjacency according to the z-axis.
    The resulting subgraphs are 2d grid graphs.
    """

    def stratified_nodes() -> AdjDict:
        """
        The adjacency should be partitioned so that the graph consists of planes of x, y,
        starting from the bottom.
        """
        return {z: {ix for ix, v in enumerate(V) if v[-1] == z} for z in sorted({vert[2] for vert in V}) if abs(z) != z}

    def filter_graph(data) -> NodesMap:
        """
        Create graph with only the data in data.
        """
        return {k: v.intersection(data) for k, v in A.items() if k in data}

    return {level: filter_graph(data) for level, data in stratified_nodes().items()}


def timed(fn):
    """
    Decorator that times a function and prints a pretty readout
    fn: function to time
    :return: fn + runtime of decorated function.
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        """
        inner function with lots of emojis.
        """
        fn_name = fn.__name__.upper()
        st = time.perf_counter()
        border = '═' + ('══' * ((len(fn.__name__) + 30) // 2))
        print()
        cp(show=True)
        print(border + '╕')
        print(f' 📌 {fn_name} | 🏁 {tstamp()}\n')
        res = fn(*args, **kwargs)
        print('\n', f'🕳 {fn_name} | 🕗 {time.perf_counter() - st:.7f} secs')
        print(border + '╛', '\n')
        return res

    return inner


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
    Run function n times
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = None
        for i in range(n):
            res = fn(*args, **kwargs)
        print(f"x{n}: {fn.__name__} took {(time.perf_counter() - start)}")
        return res

    return inner


@parametrized
def profile(func, dump=None):
    """
    cprofile decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        ORD = len(args[0])
        profiler = cProfile.Profile()
        profiler.enable()
        try:
            return_value = func(*args, **kwargs)
        finally:
            profiler.disable()
            stats = pstats.Stats(profiler)
            stats.sort_stats("tottime")
            stats.print_stats()
            prim, total = stats.__dict__['prim_calls'], stats.__dict__['total_calls']
            print(f'⭕️ {ORD}: {prim / total:.2%} primitive of {total} calls | {round(total / ORD, 2)} calls / n')
            if dump:
                stats.dump_stats(dump)
        return return_value
    return wrapper


def tstamp() -> str:
    """
    date- and timestamper
    In this format: 18:21 02/06/22
    """
    return datetime.now().strftime('%H:%M %d/%m/%y')


def unpack(nested_list) -> Unpacker:
    """
    Unpack (completely) a nested list into a generator
    """
    for nested in nested_list:
        if isinstance(nested, Iterable) and not isinstance(nested, (str, bytes)):
            yield from unpack(nested)
        else:
            yield nested


def assemble_cycle(x, y, z, snake):
    #   REMAP SOLVED TO OTHER LVLS AND WEAVE THEM INTO A CYCLE:
    prev, joined = [], []

    for ix in range(1, z, 2):
        #   FOR EVERY PAIR: REVERSE SECOND. EXTEND TO FIRST
        joined = [s + (x * y) * (ix - 1) for s in snake] + [s + (x * y) * ix for s in reversed(snake)]

        #   NEST PREVIOUS LOOP IN CURRENT LOOP
        joined[1:1] = prev[-1:] + prev[:-1]
        prev = joined

    #   RETURN JOINED
    return joined


def plot_curve_with_regression(sizes: List[int], times: List[float]):
    plt.scatter(sizes, times)
    plt.xlabel("Input sizes in millions")
    plt.ylabel("Execution times in seconds")
    coefs = np.polyfit(sizes, times, deg=2)
    der_coefs = np.polyder(coefs)
    print("Slope:", float(der_coefs[0]))
    x = np.linspace(min(sizes), max(sizes), num=100)
    y = np.polyval(coefs, x)
    predicted_times = np.polyval(coefs, sizes)
    r2 = r2_score(times, predicted_times)
    print("R^2:", r2)
    plt.plot(x, y, '-r')
    plt.show()
    plot_curve(sizes, times)


def plot_curve(sizes: List[int], times: List[float]):
    """
    Takes two inputs, a list of integers representing the x-axis values and a list of floats representing the y-axis values,
    and plots a curve using these two inputs:
    """
    plt.plot(sizes, times)
    plt.xlabel("Input sizes")
    plt.ylabel("Execution times")
    plt.show()


def get_edge_axis(edge, V) -> int:
    return next(filter(lambda i: V[edge[0]][i] != V[edge[1]][i], range(3)))


def get_points_axis(p1, p2) -> int:
    return next(filter(lambda i: p1[i] != p2[i], range(3)))


def count_nonturns(data: Path, A: AdjDict, V: Verts) -> int:
    """
    ::SNAKE VERSION::
    Counts the number of non-turns in a list of data and V.

    A non-turn is defined as a pair of edges (m, n) and (n, o) that have the same direction.

    Args:
        data: A list of indices of V in the V list.
        V: A list of 3D vector points.
        A: Adjlist
    Returns:
        The number of non-turns in the list of data and V.
    """
    count = 0
    for i in range(len(data)) if id_seq(data, A) == 'loop' else range(1, len(data) - 2):
        m, n = V[data[i - 1]], V[data[i]]
        o = V[data[0]] if i == len(data) - 1 else V[data[i + 1]]
        if (n[0] - m[0]) * (o[0] - n[0]) + (n[1] - m[1]) * (o[1] - n[1]) + (n[2] - m[2]) * (o[2] - n[2]) > 0:
            count += 1
    if not count:
        print('superperfect:', data)
    return count


def count_axes(data: List[int], V: List[Tuple[int, int, int]]) -> List[int]:
    """
    Count number of edges are in each axis.
    Return the max.
    """
    counts = [0, 0, 0]
    for i in range(len(data)):
        m, n = V[data[i - 1]], V[data[i]]
        counts[0 if m[0] != n[0] else int(m[1] != n[1]) or 2] += 1
    return min(counts)

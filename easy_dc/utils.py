import cProfile
from datetime import datetime
from functools import wraps
import os
import pickle
import pstats
import time


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


def id_seq(seq: Path, A: AdjDict) -> Certificate:
    """
    Certify sequence, return sequence type broken, loop, or snake.
    """

    if len({*seq}) != len(A) or len(seq) != len(A):
        return "💔"
    for s in range(1, len(seq)):
        if seq[s - 1] not in A[seq[s]]:
            return "💔"
    if seq[0] in A[seq[-1]]:
        return '🔁'
    return '🐍'


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


def picklesave(to_pickle, filename, show=False, space=True) -> str:
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
    return picklesave(G, os.path.join(FP_GRAPHS, str(G['ORD'])))


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

    def filter_graph(nodes) -> NodesMap:
        """
        Create graph with only the nodes in nodes.
        """
        return {k: v.intersection(nodes) for k, v in A.items() if k in nodes}

    return {level: filter_graph(nodes) for level, nodes in stratified_nodes().items()}


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
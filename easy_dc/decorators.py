import cProfile
from datetime import datetime
from functools import wraps
import pstats
import time


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
    Run function n times and timeit.
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

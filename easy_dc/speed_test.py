from itertools import pairwise

from utils.decs import times


@times(500)
def func1(data):
    return {frozenset(edge) for edge in zip(data, data[1:] + data[:1])}


@times(500)
def func2(data):
    return {frozenset(edge) for edge in pairwise(data + data[:1])}


if __name__ == '__main__':
    loop = list(range(100000))
    func1(loop)
    func2(loop)
    func1(loop)
    func2(loop)
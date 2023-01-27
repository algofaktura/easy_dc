from easy_dc.defs import *


def uon(start=8, end=3000000, n=800) -> UonGen:
    """
    Generator for the uncentered octahedral numbers.
    """
    for i in range(n + 2):
        _uon = sum([(n * (n + 2)) for n in range(0, n * 2 + 2, 2)][:i])
        if end >= _uon >= start:
            yield _uon


def absumv(n, V):
    """
    Get the accretion level of an point in a 3d grid graph.
    """
    return sum(map(abs, V[n]))


def edist(a) -> float:
    """
    Calculate the Euclidean distance between point a and the origin (0, 0, 0).
    """
    return sum([((0, 0, 0)[idx] - a[idx]) ** 2 for idx in range(len(a))]) ** 0.5


def md(a: int, b: int, V: list) -> int:
    """
    Calculate manhattan | city-block distance between nodes a and b.
    Default value for b is node 1.
    """
    vector_a, vector_b = V[a], V[b]
    return sum([abs(vector_a[i] - vector_b[i]) for i in range(len(vector_a))]) // 2


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


def count_axes(data: Path, V: Verts) -> int:
    """
    Count number of edges are in each axis.
    Return the max.
    """
    counts = [0, 0, 0]
    for i in range(len(data)):
        m, n = V[data[i - 1]], V[data[i]]
        counts[0 if m[0] != n[0] else int(m[1] != n[1]) or 2] += 1
    return min(counts)

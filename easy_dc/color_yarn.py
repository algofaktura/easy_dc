def color_yarn(length: int, vectors2d: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Receives a list of 2d vectors, and
    takes the dot product of the vectors2d and [[-1, 0], [0, -1]] and then
    adds [0, 2] to each vector, moving it in the y direction.
    """
    import numpy as np
    _reversed = np.dot(vectors2d, [[-1, 0], [0, -1]])
    return np.add(_reversed[-length:], [0, 2])


def make_weights(A: dict[int, set[int]], V: list[tuple[int, int, int]]) -> dict[int, int]:
    """
    Assign a weight to each key in A:
    returns:
        W: dict[n: int, weight: int]: W.keys() == A.keys() where the value is sum(map(abs, V[n])) which is the
        reduction of the manhattan distance where b is origin: (0, 0, 0)
    """
    return {n: sum(map(abs, V[n])) for n in A}


def strat_nodes(V):
    stratified = dict()
    for z in sorted({vert[2] for vert in V}):
        if abs(z) != z:
            stratified[z] = {ix for ix, v in enumerate(V) if v[-1] == z}
    return stratified


def filterit(nodes, adj):
    filtered = dict()
    for k, v in adj.items():
        if k in nodes:
            filtered[k] = v & nodes
    return filtered


if __name__ == '__main__':
    from easy_dc.utils.io import get_G
    order = 32
    graph = get_G(order)
    strat = strat_nodes(graph['V'])
    print(filterit(strat[-1], graph['A']))


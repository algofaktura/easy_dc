from collections import deque
from typing import Deque, Tuple, List

from easy_dc.defs import *


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

    def filter_graph(nodes: NodeSet) -> NodesMap:
        """
        Create graph with only the nodes in nodes.
        """
        return {k: v & nodes for k, v in A.items() if k in nodes}
    return {level: filter_graph(nodes) for level, nodes in stratified_nodes().items()}


def split_tour(tour: Path, subset: NodeSet) -> Paths:
    """
    Given a set S of integers representing a tour, and a subset T of S, the goal of the function is to partition S
    into multiple sublists or subtours such that:
    """
    ixs = sorted((tour.index(node) for node in subset if node in tour))
    tours, prev = [], -1
    while ixs[-1] == len(tour) - 1 and ixs[-2] == ixs[-1] - 1:
        tours.append(tour[-2:])
        tour[-2:], ixs[-2:] = [], []
    for e, ix in enumerate(ixs):
        if e == len(ixs) - 1 and ix != len(tour) - 1:
            if len(t1 := tour[prev + 1: ix]) > 1 or not t1: tours.extend((t1, tour[ix:]))
            else: tours.append(tour[prev + 1: ix + 1])
            prev = None
        elif len(t := tour[prev + 1:ix + 1]) == 1:
            if ix + 2 == len(tour) - 1:
                tours.append(tour[ix:])
                prev = None
            else:
                tours.append(tour[ix: ix + 2])
                prev = ix + 1
        else:
            tours.append(t)
            prev = ix
        if prev is None: break
    if prev is not None and (rest := tour[max(ixs) + 1:]): tours.append(rest)
    return [tour if tour[0] in subset else tour[::-1] for tour in tours if tour]


def weave_discocube(A: AdjDict, V: Verts, VI: IdxMap, EA: EAdj) -> Cycle:
    """
    The function weave takes as input an Adjacency dictionary A, a set of vertices V and an index map VI. It returns a path which represents a
    simple Hamiltonian cycle on a discocube graph.

        The function is composed of several helper functions and a class Weaver that are used to construct the Hamiltonian cycle.

        The first helper function, stratify_A, takes the input adjacency dictionary A and partitions it according to the z-axis value of the vertices.
        The resulting partitioned graph is a 2-dimensional graph in R2. It also takes advantage of the bipartite quality of the graph and cuts it in half,
        since only half a solution is solved and then mirrored to produce the full result.

        The second helper function, walk_subtours, takes the partitioned adjacency dictionary zA and a set of "bobbins" as input, and uses a "snake-walk"
        algorithm to find a path on the graph. It also uses the split_tour function that we discussed earlier to ensure that all elements of the bobbins
        set are at the first position of the subtour.

        The Weaver class has two class attributes ends and an instance attribute loom. The ends attribute is a tuple of integers representing the
        first and last element of the thread. The loom attribute is a list of deque that is used to represent the threads. The class has a method
        <set_bobbins> that sets the bobbins for the next level by adding the upper and lower neighbors of the first and last element of each thread
        in the loom attribute. The method returns a set of bobbins.

        Finally, the main body of the weave function creates an instance of the Weaver class and initializes the variable bobbins as None.
        It then iterates over the partitioned adjacency dictionary zA obtained from the stratify_A helper function. If bobbins is None, it sets it to
        the result of calling the set_bobbins method on the Weaver instance. It then calls the walk_subtours helper function with zA and bobbins as input.

        It then continues to weave the Hamiltonian cycle using the loom attribute and the set_bobbins method until all levels of the partitioned graph
        have been processed. The final path obtained is returned as the result of the weave function.
    """
    class Weaver:
        """
        The Weaver class is a helper class used in the weave function. It has two class attributes ends and an instance attribute loom.

            ends is a tuple of integers representing the first and last element of the thread.
            loom is a list of deque that is used to represent the threads.

        The class has a method set_bobbins that takes no arguments and returns a set of bobbins. it sets the bobbins for the next level by adding
        the upper and lower neighbors of the first and last element of each thread in the loom attribute.

        The method iterates over the loom attribute and for each thread in loom it adds the upper and lower neighbors of the first and last element
        respectively, to the bobbins set.

        It also adds the upper and lower neighbors to the thread by using the appendleft() and append() functions of the deque structure respectively.
        The bobbins set is used later in the weave function to ensure that all elements of the bobbins set are at the first position of the subtour
        obtained from the walk_subtours helper function.
        """
        ends: Tuple[int] = 0, -1
        loom: List[Deque[int]] = []

        def set_bobbins(self) -> NodeSet:
            bobbins = set()
            for thread in self.loom:
                for end in self.ends:
                    bobbins.add(upper := VI[(vector := V[thread[end]])[0], vector[1], vector[2] + 2])
                    if not end: thread.appendleft(upper)
                    else: thread.append(upper)
            return bobbins

    class Warp:
        """
        Simple class to for sequences as edges and their adjacency.
        Rotates seq according to edge and joins them.
        """
        def __init__(self, data):
            self.data = list(data)
            self.set = False

        @property
        def edges(self): return {frozenset(edge) for edge in zip(self.data, self.data[1:] + self.data[:1])}

        @property
        def adjs(self): return {aedge for edge in self.edges for aedge in EA[edge]}

        def join(self, edge=None, oedge=None, other=None):
            self.rotate_to_edge(*edge)
            other.rotate_to_edge(*(oedge if oedge[0] in A[edge[-1]] else oedge[::-1]))
            self.data[len(self.data):] = other.data[:]
            other.set, other.data = True, None

        def rotate_to_edge(self, start, end):
            """
            Rotates loop so that the ends are the edge.
            should be done in one step.
            """
            if start == self.data[-1] and end == self.data[0]: self.data[:] = self.data[::-1]
            elif (idx_start := self.data.index(start)) > (idx_end := self.data.index(end)): self.data[:] = self.data[idx_start:] + self.data[:idx_start]
            else: self.data[:] = self.data[idx_end - 1::-1] + self.data[:idx_end - 1:-1]

    def stratify_A() -> GLvls:
        """
        Partition the Adjacency according to the z-axis.
        The resulting subgraphs are 2d grid graphs.
        """
        def stratified_nodes() -> AdjDict:
            """
            The adjacency should be partitioned so that the graph consists of planes of x, y,
            starting from the bottom.
            """
            return {z: {idx for idx, v in enumerate(V) if v[-1] == z} for z in sorted({vert[2] for vert in V}) if abs(z) != z}

        def filter_graph(nodes) -> NodesMap:
            """
            Create graph with only the nodes in nodes.
            """
            return {k: v.intersection(nodes) for k, v in A.items() if k in nodes}

        return {level: filter_graph(nodes) for level, nodes in stratified_nodes().items()}

    def walk_subtours(zA: AdjDict, bobbins: NodeSet = None) -> Paths:
        """
        Snake walk as small algo
        """
        path, w = [max(zA)], {n: sum(map(abs, V[n])) for n in zA}
        for _ in range(len(zA) - 1): path.append(sorted(zA[path[-1]] - {*path}, key=lambda n: w[n]).pop())
        return [path] if bobbins is None else split_tour(path, bobbins)

    def set_loom():
        """
        Place warp threads in loop
        """
        weaver = Weaver()
        bobbins = None
        for z, zA in stratify_A().items():
            joined, warps = set(), walk_subtours(zA, bobbins=bobbins)
            if bobbins:
                for thread in weaver.loom:
                    for end in weaver.ends:
                        connector = thread.pop() if end else thread.popleft()
                        for ix, warp in enumerate(warps):
                            if ix not in joined:
                                if connector == warp[0]:
                                    if end: thread.extend(warp)
                                    else: thread.extendleft(warp)
                                    joined.add(ix)
            weaver.loom.extend((deque(weft) for weft in (w for ix, w in enumerate(warps) if ix not in joined)))
            bobbins = set(weaver.set_bobbins()) if z != -1 else None
        for w in weaver.loom: w.extend([VI[(vector := V[node])[0], vector[1], -vector[2]] for node in reversed(w)])
        return weaver.loom

    def weave(warps):
        """
        Interweave weft with warps
        """
        warps = [Warp(warp) for idx, warp in enumerate(warps)]
        for warp in warps:
            if warp.set: continue
            for other in warps:
                if warp != other and not other.set:
                    if loop2other := warp.edges & other.adjs:
                        if other_edges := EA[edge := loop2other.pop()] & other.edges:
                            warp.join(edge=tuple(edge), oedge=tuple(other_edges.pop()), other=other)
        return [warp.data for warp in warps if not warp.set]
    to_weave = list((s for s in sorted(set_loom(), key=len, reverse=True)))
    return weave(to_weave).pop()

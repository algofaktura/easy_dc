from collections import deque
from itertools import combinations

from easy_dc.defs import *


def weave_discocube(A: AdjDict, V: Verts, VI: IdxMap, EA: EAdj, W: Weights, ZA: GLvls) -> Solution:
    """
    Solves the hamiltonian cycle problem in discocube graphs deterministically and in linear time by divide and conquer.

    As the size of the input grows, the time it takes to solve the problem increases by a factor proportional to the input.
    The function weave takes as input an Adjacency dictionary A, a set of vertices V and an index map VI and a weights W.
    It returns a path representing Hamiltonian cycle on a discocube graph.
    This algorithm can also be used on diamond-shaped hexagonal prismatic honeycombs which can be accessed by the ORD = 4620

    AdjDict = Dict[int, Set[int]]: Adjacency list of index representation of vectors in the list V.
    Verts = Tuple[Tuple[int, int, int]]: Tuple of vectors.
    IdxMap = Dict[Any, int]: Maps vectors to their indices to avoid costly index lookups.
    EAdj = Dict[FrozenSet[int], Set[FrozenSet[int]]]: Adjacent edges of an edge, ie., parallel to the key edge and 1 unit length distance away.
    Weights = Dict[int, Union[int, float]]: Weights for each node based on their accretion level.
    GLvls = Dict[int, Dict[str, Any]]: The adjacency dictionary partitioned according to their x value, so that they are planes of x, y.
    """

    class Weaver:
        """
        General weaver class with a loom and prepares threads to connect to one another.
        """
        ends: Ends = 0, -1
        loom: Loom = []

        @staticmethod
        def spin(zA: AdjDict) -> Path:
            """
            If the start node is either the centermost or the outermost node, it can walk all paths without backtracking.
            """
            spool = [max(zA)]
            warp_length = len(zA) - 1
            for _ in range(warp_length):
                spool.append(sorted(zA[spool[-1]] - {*spool}, key=lambda n: W[n])[-1])
            return spool

        @staticmethod
        def split(tour: Path, subset: NodeSet) -> Paths:
            """
            Given a set S of integers representing a tour, and a subset T of S, the goal is to partition the tour
            into the least number of subtours such that the length of each subtour is longer than 2 unless the subtour consists of
            a node from the subset. At least one node from the subset (if there are more than subset node in the subtour)
            in the subtour is in the first index (as a result of reversing the sequence) to facilitate extending to the loom threads.
            """
            subtours, prev = [], -1
            last_idx = len(tour) - 1
            while (ixs := sorted((tour.index(node) for node in subset)))[-1] == last_idx and ixs[-2] == ixs[-1] - 1:
                subtours.append(tour[-2:])
                tour[-2:], ixs[-2:] = [], []
            for e, ix in enumerate(ixs):
                if e == len(ixs) - 1 and ix != last_idx:
                    if len(t1 := tour[prev + 1: ix]) > 1 or not t1:
                        subtours.extend((t1, tour[ix:]))
                    else:
                        subtours.append(tour[prev + 1: ix + 1])
                    prev = None
                else:
                    subtours.append(tour[prev + 1:ix + 1])
                    prev = ix
                if prev is None:
                    break
            if prev and (rest := tour[max(ixs) + 1:]):
                subtours.append(rest)
            return [tour if tour[0] in subset else tour[::-1] for tour in subtours if tour]

        def weave(self) -> Solution:
            """
            Interweave weft with warps i.e., join loops together.
            """
            loom = {idx: Loop(warp) for idx, warp in enumerate(self.warp_loom())}
            while len(loom) > 1:
                for ix_warp, ix_weft in combinations(loom.keys(), 2):
                    if bridge := (warp := loom[ix_warp]).edges & (weft := loom[ix_weft]).eadjs:
                        if weft_edges := EA[warp_edge := bridge.pop()] & weft.edges:
                            warp.join(edge=tuple(warp_edge), oedge=tuple(weft_edges.pop()), other=loom.pop(ix_weft))
                            break
            return loom[0].loop

        def warp_loom(self) -> Loom:
            """
            Place warp threads in loop ie., Warping.
            """
            bobbins = None
            for z, zA in ZA.items():
                yarn = Weaver.spin(zA)
                woven, warps = set(), Weaver.split(yarn, bobbins) if bobbins else [yarn]
                for thread in self.loom:
                    for end in self.ends:
                        for ix, warp in enumerate(warps):
                            if ix not in woven:
                                if thread[end] == warp[0]:
                                    woven.add(ix)
                                    if end:
                                        thread.extend(warp[1:])
                                    else:
                                        thread.extendleft(warp[1:])
                self.loom.extend((deque(warp) for warp in (w for ix, w in enumerate(warps) if ix not in woven)))
                bobbins = {*self.set_bobbins()} if z != -1 else None
            for w in self.loom:
                w.extend([VI[(vector := V[node])[0], vector[1], -vector[2]] for node in reversed(w)])
            return sorted(self.loom)

        def set_bobbins(self) -> NodeSet:
            """
            returns a set of bobbins. it sets the bobbins for the next level by adding the upper and lower neighbors of the first and last element
            of each thread in the loom attribute. The method iterates over the loom attribute and for each thread in loom it adds the upper and lower
            neighbors of the first and last element respectively, to the bobbins set.
            """
            bobbins: NodeSet = set()
            for thread in self.loom:
                for end in self.ends:
                    bobbins.add(upper := VI[(vector := V[thread[end]])[0], vector[1], vector[2] + 2])
                    if not end:
                        thread.appendleft(upper)
                    else:
                        thread.append(upper)
            return bobbins

    class Loop:
        """
        Simple loop class with an edges property: the sequence as a set of edges, or
        an edges adj: all the adjacent edges of the loop, ie are parallel to the individual edges of the loop.
        """

        def __init__(self, loop):
            self.loop: Path = list(loop)

        @property
        def edges(self) -> FrozenEdges:
            """
            The current loop represented as a set of frozensets of edges.
            [0, 1, 2, 3] -> {frozenset([0, 1]), frozenset([1, 2]), frozenset([2, 3]), frozenset([3, 0])}
            """
            return {frozenset(edge) for edge in zip(self.loop, self.loop[1:] + self.loop[:1])}

        @property
        def eadjs(self) -> FrozenEdges:
            """
            Edges parallel to and one unit length distance away from each edge in self.edges.
            """
            return {eadj for edge in self.edges for eadj in EA[edge]}

        def join(self, edge=None, oedge=None, other=None):
            """
            Rotate loop according to edge and merely extend to the end.
            """
            self.rotate_to_edge(*edge)
            other.rotate_to_edge(*(oedge if oedge[0] in A[edge[-1]] else oedge[::-1]))
            self.loop.extend(other.loop)

        def rotate_to_edge(self, start: int, end: int):
            """
            Rotates loop so that the edge are the matches the ends of the loop:
            Edge (1, 7) -> Loop (1, 3, 4, 5, 6, 2, 7)
            """
            if start == self.loop[-1] and end == self.loop[0]:
                self.loop[:] = self.loop[::-1]
            elif (ix_start := self.loop.index(start)) > (ix_end := self.loop.index(end)):
                self.loop[:] = self.loop[ix_start:] + self.loop[:ix_start]
            else:
                self.loop[:] = self.loop[ix_end - 1::-1] + self.loop[:ix_end - 1:-1]

    return Weaver().weave()

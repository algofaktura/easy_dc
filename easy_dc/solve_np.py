"""
How to weave tapestry.

1.  Spinning the yarn:
The first step in making a tapestry is to create the yarn that will be used in the weaving process. This can be done by spinning raw fibers such
as wool or cotton into long, thin strands using a spinning wheel or other tool.

2.  Setting up the loom:
Once the yarn has been spun, the next step is to set up the loom on which the tapestry will be woven. This typically involves stretching a series
of parallel threads, called the warp, across the loom, and attaching them to the loom's frame.

3.  Threading the warp:
Next, the yarn that was spun in step 1 is threaded through the warp threads, starting at the top of the loom and working down to the bottom.
This process is called threading the warp.

4.  Weaving the weft:
After the warp has been threaded, the weaver begins the process of weaving the weft, which is the yarn that will be used to create the design
on the tapestry. This is done by using a shuttle to pass the weft yarn over and under the warp threads, following a predetermined pattern.

5.  Adding the weft:
The weaver then adds the weft yarn to the loom by passing it over and under the warp threads. The weaver uses a comb to push the weft yarn
tight against the previous row of weft yarn and to keep the warp threads straight.

6.  Repeating the process:
The weaver continues to add weft yarn, following the predetermined pattern, until the tapestry is the desired size. The weaver will continue
to repeat the process of adding weft yarn to the loom until the tapestry is complete.

7.  Removing the tapestry:
Once the tapestry is complete, it is removed from the loom. The tapestry is then ready to be used or displayed.
"""
from collections import deque
from itertools import combinations

import numpy as np

from easy_dc.defs import *
from easy_dc.utils import profile


@profile()
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
            self.loop += other.loop

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

    def weave() -> Solution:
        """
        Weave the weft.
        len of loom is very small:
        for a graph with n vertices:
            n            loops in loom
            79_040   ->  20
            273_760  ->  30
            540_200  ->  37
            762_272  ->  42
        """
        loom = {idx: Loop(warp) for idx, warp in enumerate(warp_loom())}
        while len(loom) > 1:
            for ix_warp, ix_weft in combinations(loom.keys(), 2):
                if bridge := (warp := loom[ix_warp]).edges & (weft := loom[ix_weft]).eadjs:
                    if weft_edges := EA[warp_edge := bridge.pop()] & weft.edges:
                        warp.join(edge=tuple(warp_edge), oedge=tuple(weft_edges.pop()), other=loom.pop(ix_weft))
                        break
        return loom[0].loop

    def warp_loom() -> Loom:
        """
        Warping.
        Setting up the loom.
        Place warp threads in loom.
        Thread the warp.
        """
        loom = []
        bobbins = None
        for z, zA in ZA.items():
            woven = set()
            yarn = get_yarn(z, zA)
            warps = split(yarn, bobbins) if bobbins else [yarn]
            for thread in loom:
                for ix, warp in enumerate(warps):
                    for end in ends:
                        if ix not in woven:
                            if thread[end] == warp[0]:
                                woven.add(ix)
                                if end:
                                    thread.extend(warp[1:])
                                else:
                                    thread.extendleft(warp[1:])
            loom.extend((deque(warp) for warp in (w for ix, w in enumerate(warps) if ix not in woven)))
            bobbins = {*set_bobbins(loom)} if z != -1 else None
        for w in loom:
            w.extend([VI[(vector := V[node])[0], vector[1], -vector[2]] for node in reversed(w)])
        return sorted(loom)

    def spin(zA: AdjDict) -> Path:
        """
        If the start node is either the centermost or the outermost node, it can walk all paths without backtracking.
        """
        spool = [max(zA)]
        warp_length = len(zA) - 1
        for _ in range(warp_length):
            spool.append(sorted(zA[spool[-1]] - {*spool}, key=lambda n: W[n])[-1])
        return spool

    def color_yarn():
        """
        Get colored yarns for weaving.
        """
        return (red := [V[node][:2] for node in spin(ZA[-1])]), np.add(np.dot(np.array(red), np.array([[-1, 0], [0, -1]]))[-len(ZA[-3]):], [0, 2])

    def get_yarn(zlevel, zA):
        """
        Get the yarn from the spool
        returns generator.
        yarn color will have to be passed in by the caller, so it must know.. or should i have a map so i can find out what?

        I need to know which rotation this level belongs.
        """
        return [VI[(*xy, zlevel)] for xy in (red_yarn if zlevel in red else blue_yarn)[-len(zA):]]

    def color_levels():
        """
        unzip a list into two lists
        first list has the highest value: which is the level from which to to add to the z value
        """
        return (revZA := list(reversed(ZA)))[::2], revZA[1::2]

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
            subtours += [tour[-2:]]
            tour[-2:], ixs[-2:] = [], []
        for e, ix in enumerate(ixs):
            if e == len(ixs) - 1 and ix != last_idx:
                if len(t1 := tour[prev + 1: ix]) > 1 or not t1:
                    subtours += (t1, tour[ix:])
                else:
                    subtours += [tour[prev + 1: ix + 1]]
                prev = None
            else:
                subtours += [tour[prev + 1:ix + 1]]
                prev = ix
            if prev is None:
                break
        if prev and (rest := tour[max(ixs) + 1:]):
            subtours += [rest]
        return [tour if tour[0] in subset else tour[::-1] for tour in subtours if tour]

    def set_bobbins(loom: Loom) -> NodeSet:
        """
        returns a set of bobbins. it sets the bobbins for the next level by adding the upper and lower neighbors of the first and last element
        of each thread in the loom. The method iterates over the threads in the loom and adds the upper and lower
        neighbors of the first and last element respectively, to the bobbins set and to the ends of the thread.
        """
        bobbins: NodeSet = set()
        for thread in loom:
            for end in ends:
                bobbins.add(upper := VI[(vector := V[thread[end]])[0], vector[1], vector[2] + 2])
                if not end:
                    thread.appendleft(upper)
                else:
                    thread.append(upper)
        return bobbins

    ends: Ends = 0, -1
    red, blue = color_levels()
    red_yarn, blue_yarn = color_yarn()
    return weave()


if __name__ == '__main__':
    from utils import get_G, save_G, stratify_A, id_seq, uon

    for order in uon(632632, 632632):
        # order = 2997280
        G = get_G(order)
        A, V, VI, E, EA = G['A'], G['V'], G['VI'], G['E'], G['EA']
        G['W'] = W = {n: sum(map(abs, V[n])) for n in A}
        G['ZA'] = ZA = stratify_A(A, V)
        lst = list(reversed(ZA.keys()))
        save_G(G)
        print("solving order ", order)
        woven = weave_discocube(A, V, VI, EA, W, ZA)
        print(f'⭕️ {order}')
        print('💰', len(woven), id_seq(woven, A))

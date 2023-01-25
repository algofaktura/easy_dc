import numpy as np

from collections import deque
from itertools import combinations, pairwise

from easy_dc.defs import *
from easy_dc.utils import profile, timed, time, count_nonturns, count_axes  # noqa


def weave_solution(A: AdjDict, V: Verts, VI: IdxMap, EA: EAdj, W: Weights, ZA: GLvls) -> Solution:
    """
    Solves the hamiltonian cycle problem in discocube graphs deterministically using divide and conquer (non-recursive) and in linear time (the time it takes grows to solve the problem grows linearly to the size of the input) . Uses the weaving process as inspiration and metaphor for the algorithmic design and process.
    1. Spin yarn: create an initial hamiltonian path from the node furthest from the origin to the origin
    2. color yarn: each level alternates in color from red to blue. The blue yarn is a 180 rotation around the z-axis and a unit length displacement
    in the y direction.

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
    ends: Ends = 0, -1

    class Loop:
        """
        Simple loop class with an edges property: the sequence as a set of edges, or
        an edges adj: all the adjacent edges of the loop, ie are parallel to the individual edges of the loop.
        """

        def __init__(self, loop):
            self.loop: Path = list(loop)
            self.looped = None
            self._eadjs = None

        @property
        def edges(self):
            """
            The current loop represented as a set of frozensets of edges.
            [0, 1, 2, 3] -> {frozenset([0, 1]), frozenset([1, 2]), frozenset([2, 3]), frozenset([3, 0])}
            """
            return {frozenset(edge) for edge in pairwise(self.loop + self.loop[:1])}

        @property
        def eadjs(self) -> FrozenEdges:
            """
            Edges parallel to and one unit length distance away from each edge in self.edges.
            """
            if self.loop != self.looped:
                self._eadjs = {eadj for edge in self.edges for eadj in EA[edge]}
                self.looped = self.loop[:]
            return self._eadjs

        def join(self, edge=None, oedge=None, other=None):
            """
            Rotate loop according to edge and merely extend to the end.
            """
            self.rotate_to_edge(*edge)
            other.rotate_to_edge(*(oedge if oedge[0] in A[edge[-1]] else oedge[::-1]))
            self.loop[len(self.loop):] = other.loop

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
        loom = warp_loom()
        while len(loom) > 1:
            for ix_warp, ix_weft in combinations(loom.keys(), 2):
                if bridge := (warp := loom[ix_warp]).edges & (weft := loom[ix_weft]).eadjs:
                    if weft_edges := EA[warp_edge := bridge.pop()] & weft.edges:
                        warp.join(edge=tuple(warp_edge), oedge=tuple(weft_edges.pop()), other=loom.pop(ix_weft))
                        break
        return loom[0].loop

    def warp_loom() -> WarpedLoom:
        """
        Warping.
        Setting up the loom.
        Place warp threads in loom.
        Thread the warp.
        """
        rb_yarn = {
            3: (red := [V[node][:2] for node in spin(ZA[-1])]),
            1: np.add(np.dot(np.array(red), [[-1, 0], [0, -1]])[-len(ZA[-3]):], [0, 2])
        }
        bobbins, loom = None, []
        for z, zA in ZA.items():
            woven = set()
            yarn = [VI[(*xy, z)] for xy in rb_yarn[z % 4][-len(zA):]]
            warps = cut(yarn, bobbins) if bobbins else [yarn]
            for thread in loom:
                for ix, warp in enumerate(warps):
                    if ix not in woven:
                        for end in ends:
                            if thread[end] == warp[0]:
                                woven.add(ix)
                                if end:
                                    thread.extend(warp[1:])
                                else:
                                    thread.extendleft(warp[1:])
            loom.extend((deque(warp) for warp in (w for ix, w in enumerate(warps) if ix not in woven)))
            bobbins = {*wind_bobbins(loom)} if z != -1 else None
        for w in loom:
            w += [VI[(vector := V[node])[0], vector[1], -vector[2]] for node in reversed(w)]
        return {idx: Loop(warp) for idx, warp in enumerate(sorted(loom))}

    def spin(zA: AdjDict) -> Path:
        """
        Walk a hamiltonian circuit starting from the node furthest from origin to towards the node closest to origin without backtracking by using
        the calculating the attrition factor and ordering the next steps accordingly. When calculating this factor, if the start node is either the
        centermost or the outermost node, it can walk all paths without backtracking.

        spin() -> yarn: walk a hamiltonian circuit starting from the node furthest from origin to towards the node closest to origin. One should find
        the hamiltonian path from the largest level in order to produce the longest piece of yarm. If the initial tour came from the least nodes ie.,
        min(vector[2]) it would result in only a tour with four nodes, which is useless in creating other tours.
        """
        spool = [max(zA)]
        warp_length = len(zA) - 1
        for _ in range(warp_length):
            spool.append(sorted(zA[spool[-1]] - {*spool}, key=lambda n: W[n])[-1])
        return spool

    def cut(tour: Path, subset: NodeSet) -> Paths:
        """
        Given a set S of integers representing a tour, and a subset T of S, the goal is to partition the tour
        into the least number of subtours such that the length of each subtour is longer than 2 unless the subtour consists of
        a node from the subset. At least one node from the subset (if there are more than subset node in the subtour)
        in the subtour is in the first index (as a result of reversing the sequence) to facilitate extending to the loom threads.

        number of bobbins increases by 2 as the level grows:

        ixs = sorted((tour.index(node) for node in subset))
        print(ixs):

            [8, 11]
            [14, 19]
            [20, 25, 27, 36]
            [26, 33, 35, 48, 55, 56]
            [32, 41, 43, 62, 71, 80]
            [38, 49, 51, 76, 87, 100, 107, 108]
            [44, 57, 59, 90, 103, 122, 131, 140]
            [50, 65, 67, 104, 119, 144, 155, 168, 175, 176]
            [56, 73, 75, 118, 135, 166, 179, 198, 207, 216]
            [62, 81, 83, 132, 151, 188, 203, 228, 239, 252, 259, 260]
            [68, 89, 91, 146, 167, 210, 227, 258, 271, 290, 299, 308]
            [74, 97, 99, 160, 183, 232, 251, 288, 303, 328, 339, 352, 359, 360]
            [80, 105, 107, 174, 199, 254, 275, 318, 335, 366, 379, 398, 407, 416]
            [86, 113, 115, 188, 215, 276, 299, 348, 367, 404, 419, 444, 455, 468, 475, 476]
            [92, 121, 123, 202, 231, 298, 323, 378, 399, 442, 459, 490, 503, 522, 531, 540]
            [98, 129, 131, 216, 247, 320, 347, 408, 431, 480, 499, 536, 551, 576, 587, 600, 607, 608]
            [104, 137, 139, 230, 263, 342, 371, 438, 463, 518, 539, 582, 599, 630, 643, 662, 671, 680]
            [110, 145, 147, 244, 279, 364, 395, 468, 495, 556, 579, 628, 647, 684, 699, 724, 735, 748, 755, 756]
            [116, 153, 155, 258, 295, 386, 419, 498, 527, 594, 619, 674, 695, 738, 755, 786, 799, 818, 827, 836]
            [122, 161, 163, 272, 311, 408, 443, 528, 559, 632, 659, 720, 743, 792, 811, 848, 863, 888, 899, 912, 919, 920]
            [128, 169, 171, 286, 327, 430, 467, 558, 591, 670, 699, 766, 791, 846, 867, 910, 927, 958, 971, 990, 999, 1008]
            [134, 177, 179, 300, 343, 452, 491, 588, 623, 708, 739, 812, 839, 900, 923, 972, 991, 1028, 1043, 1068, 1079, 1092, 1099, 1100]
            [140, 185, 187, 314, 359, 474, 515, 618, 655, 746, 779, 858, 887, 954, 979, 1034, 1055, 1098, 1115, 1146, 1159, 1178, 1187, 1196]
        """
        subtours, prev = [], -1
        last_idx = len(tour) - 1
        for e, ix in enumerate(ixs := sorted((tour.index(node) for node in subset))):
            if e == len(ixs) - 1 and ix != last_idx:
                if len(t1 := tour[prev + 1: ix]) > 1 or not t1:
                    subtours += [t1, tour[ix:]]
                else:
                    subtours += [tour[prev + 1: ix + 1]]
            else:
                subtours += [tour[prev + 1:ix + 1]]
                prev = ix
        return [tour if tour[0] in subset else tour[::-1] for tour in subtours if tour]

    def wind_bobbins(loom: Loom) -> NodeSet:
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

    return weave()


def main():
    from utils import get_G, id_seq, uon

    uon_range = 9120, 9120
    orders = []
    all_times = []
    for order in uon(*uon_range):
        G = get_G(order)
        A, V, VI, E, EA, W, ZA = G['A'], G['V'], G['VI'], G['E'], G['EA'], G['W'], G['ZA']
        ord_times = []
        assert order == len(A)
        woven = None
        for _ in range(50):
            start = time.time()
            woven = weave_solution(A, V, VI, EA, W, ZA)
            nonturns = count_nonturns(woven, A, V)
            ax = count_axes(woven, V)
            print('NONTURNS:', nonturns, '|', 'AXES:', ax, len(woven))
            dur = time.time() - start
            # print(f'⏱️ {dur:.7f} ')
            ord_times.append(dur)
        all_times.append(min(ord_times))
        orders.append(order / 1000000)
        print(f'⭕️ {order:>7} | ⏱️ {all_times[-1]:.7f} | "🩺", {len(woven)}/{order}: {id_seq(woven, A)}')

    print(f'orders = {orders}')
    print(f'all_times = {all_times}')


if __name__ == '__main__':
    main()
import numpy as np
from collections import deque

from defs import *
from utils.decs import profile


@profile()
def weave_solution(A: AdjDict, V: Verts, VI: IdxMap, EA: EAdj, W: Weights, ZA: GLvls) -> Solution:
    """
    Solves the hamiltonian cycle problem in discocube graphs deterministically using divide and conquer (
    non-recursive) and in linear time (the time it takes grows to solve the problem grows linearly to the size of the
    input) . Uses the weaving process as inspiration and metaphor for the algorithmic design and process.
    1. Spin yarn: create an initial hamiltonian path from the node furthest from the origin to the origin
    2. color yarn: each level alternates in color from natural to blue. The blue yarn is a 180 rotation around the
    z-axis and a unit length displacement
    in the y direction.

    As the size of the input grows, the time it takes to solve the problem increases by a factor proportional to the
    input.
    The function weave takes as input an Adjacency dictionary A, a set of vertices V and an index map VI and a
    weights W.
    It returns a path representing Hamiltonian cycle on a discocube graph.
    This algorithm can also be used on diamond-shaped hexagonal prismatic honeycombs which can be accessed by the ORD
    = 4620

    Vector version (using vectors instead of nodes (indices of vectors)) doesn't make it any faster.
    AdjDict = Dict[int, Set[int]]: Adjacency list of index representation of vectors in the list V.
    Verts = Tuple[Tuple[int, int, int]]: Tuple of vectors.
    IdxMap = Dict[Any, int]: Maps vectors to their indices to avoid costly index lookups.
    EAdj = Dict[FrozenSet[int], Set[FrozenSet[int]]]: Adjacent edges of an edge, ie., parallel to the key edge and 1
    unit length distance away.
    Weights = Dict[int, Union[int, float]]: Weights for each node based on their accretion level.
    GLvls = Dict[int, Dict[str, Any]]: The adjacency dictionary partitioned according to their x value, so that they
    are planes of x, y.
    """

    class Loop:
        """
        Loop Class for representing a data of edges.

        Attributes:
            data (list): A list of edges that represent the data.
            looped (list): A copy of the data attribute to check if the data has been modified.
            _eadjs (set): Set of edges that are parallel to and one unit length away from each edge in self.edges.

        Methods:
            join: Rotates the data according to an edge and extends it to the end.
            rotate_to_edge: Rotates the data so that the edge matches the ends of the data.

        Properties:
            edges: returns the current data represented as a set of frozensets of edges.
            eadjs: returns edges parallel to and one unit length distance away from each edge in self.edges.
        """

        def __init__(self, data, lead=False):
            self.lead = lead
            self.data: Path = list(data)
            self.joined = False
            self.looped = None
            self._eadjs = None
            self._edges = None
            self.last = False
            self.prev = False

        @property
        def edges(self):
            """
            The current data represented as a set of frozensets of edges.

            [0, 1, 2, 3] -> {frozenset([0, 1]), frozenset([1, 2]), frozenset([2, 3]), frozenset([3, 0])}
            Calculated all the time as the self.data value constantly changes.

            If index == 0, meaning the data is the main data (into which all other loops are incorporated)

            There is a pattern i'm still trying to get at to reduce the time by knowing exactly where to stitch:
            (30, 31) [(3, 1, -1), (3, 1, 1)] (7, 6) [(1, 1, 1), (1, 1, -1)]
            (24, 76) [(1, 1, -3), (1, 1, -5)] (124, 52) [(3, 1, -5), (3, 1, -3)]
            (400, 190) [(1, 1, -9), (1, 1, -7)] (258, 468) [(3, 1, -7), (3, 1, -9)]
            (1157, 701) [(1, 1, 13), (1, 1, 11)] (801, 1285) [(3, 1, 11), (3, 1, 13)]
            (2568, 1800) [(1, 1, -17), (1, 1, -15)] (1892, 2720) [(3, 1, -15), (3, 1, -17)]
            (3601, 4845) [(1, 1, 19), (1, 1, 21)] (4989, 3765) [(3, 1, 21), (3, 1, 19)]
            (6388, 8196) [(1, 1, -23), (1, 1, -25)] (8372, 6612) [(3, 1, -25), (3, 1, -23)]
            (10297, 12789) [(1, 1, 27), (1, 1, 29)] (13005, 10509) [(3, 1, 29), (3, 1, 27)]
            (18868, 15524) [(1, 1, -33), (1, 1, -31)] (15828, 19152) [(3, 1, -31), (3, 1, -33)]
            (26497, 22453) [(1, 1, 37), (1, 1, 35)] (22653, 26849) [(3, 1, 35), (3, 1, 37)]
            (31064, 36006) [(1, 1, -39), (1, 1, -41)] (36366, 31296) [(3, 1, -41), (3, 1, -39)]
            (47737, 41653) [(1, 1, 45), (1, 1, 43)] (42009, 47973) [(3, 1, 43), (3, 1, 45)]
            (54296, 61532) [(1, 1, -47), (1, 1, -49)] (61920, 54784) [(3, 1, -49), (3, 1, -47)]
            (77912, 69508) [(1, 1, -53), (1, 1, -51)] (69860, 78364) [(3, 1, -51), (3, 1, -53)]
            (86992, 96924) [(1, 1, -55), (1, 1, -57)] (97412, 87368) [(3, 1, -57), (3, 1, -55)]
            (107600, 118804) [(1, 1, -59), (1, 1, -61)] (119300, 108096) [(3, 1, -61), (3, 1, -59)]
            (130797, 143773) [(1, 1, 63), (1, 1, 65)] (144173, 131305) [(3, 1, 65), (3, 1, 63)]
            (157421, 171957) [(1, 1, 67), (1, 1, 69)] (172357, 158025) [(3, 1, 69), (3, 1, 67)]
            (187152, 203632) [(1, 1, -71), (1, 1, -73)] (204296, 187696) [(3, 1, -73), (3, 1, -71)]
            (220937, 238997) [(1, 1, 75), (1, 1, 77)] (239821, 221449) [(3, 1, 77), (3, 1, 75)]
            (258045, 278245) [(1, 1, 79), (1, 1, 81)] (278717, 258621) [(3, 1, 81), (3, 1, 79)]
            (299321, 321517) [(1, 1, 83), (1, 1, 85)] (322149, 300061) [(3, 1, 85), (3, 1, 83)]
            (344848, 368712) [(1, 1, -87), (1, 1, -89)] (369464, 345264) [(3, 1, -89), (3, 1, -87)]
            (394464, 420972) [(1, 1, -91), (1, 1, -93)] (421708, 395236) [(3, 1, -93), (3, 1, -91)]
            (477833, 448925) [(1, 1, 97), (1, 1, 95)] (449653, 478629) [(3, 1, 95), (3, 1, 97)]
            (507832, 539348) [(1, 1, -99), (1, 1, -101)] (540072, 508544) [(3, 1, -101), (3, 1, -99)]
            (572108, 606140) [(1, 1, -103), (1, 1, -105)] (606736, 573040) [(3, 1, -105), (3, 1, -103)]
            (677681, 640989) [(1, 1, 109), (1, 1, 107)] (642037, 678625) [(3, 1, 107), (3, 1, 109)]
            (755312, 716148) [(1, 1, -113), (1, 1, -111)] (716752, 756352) [(3, 1, -111), (3, 1, -113)]
            (795993, 838833) [(1, 1, 115), (1, 1, 117)] (839693, 796873) [(3, 1, 117), (3, 1, 115)]
            (920377, 880097) [(1, 1, 121), (1, 1, 119)] (880849, 921397) [(3, 1, 119), (3, 1, 121)]
            (958668, 995764) [(1, 1, -123), (1, 1, -125)] (996288, 959520) [(3, 1, -125), (3, 1, -123)]
            (1063625, 1030709) [(1, 1, 129), (1, 1, 127)] (1031389, 1064249) [(3, 1, 127), (3, 1, 129)]
            (1094905, 1124029) [(1, 1, 131), (1, 1, 133)] (1124709, 1095477) [(3, 1, 133), (3, 1, 131)]
            (1151668, 1176388) [(1, 1, -135), (1, 1, -137)] (1176872, 1152072) [(3, 1, -137), (3, 1, -135)]
            (1199161, 1219345) [(1, 1, 139), (1, 1, 141)] (1219653, 1199549) [(3, 1, 141), (3, 1, 139)]
            (1253580, 1237772) [(1, 1, -145), (1, 1, -143)] (1238180, 1253812) [(3, 1, -143), (3, 1, -145)]
            (1280425, 1267633) [(1, 1, 149), (1, 1, 147)] (1267821, 1280613) [(3, 1, 147), (3, 1, 149)]
            (1301832, 1291684) [(1, 1, -153), (1, 1, -151)] (1291848, 1301972) [(3, 1, -151), (3, 1, -153)]
            (1319457, 1311101) [(1, 1, 157), (1, 1, 155)] (1311249, 1319645) [(3, 1, 155), (3, 1, 157)]
            (1326961, 1333513) [(1, 1, 159), (1, 1, 161)] (1333653, 1327077) [(3, 1, 161), (3, 1, 159)]
            (1339440, 1344696) [(1, 1, -163), (1, 1, -165)] (1344764, 1339556) [(3, 1, -165), (3, 1, -163)]
            (1349377, 1353481) [(1, 1, 167), (1, 1, 169)] (1353549, 1349469) [(3, 1, 169), (3, 1, 167)]
            (1357008, 1360032) [(1, 1, -171), (1, 1, -173)] (1360076, 1357052) [(3, 1, -173), (3, 1, -171)]
            (1364880, 1362648) [(1, 1, -177), (1, 1, -175)] (1362692, 1364924) [(3, 1, -175), (3, 1, -177)]
            (1366752, 1368336) [(1, 1, -179), (1, 1, -181)] (1368380, 1366796) [(3, 1, -181), (3, 1, -179)]
            (1370737, 1369657) [(1, 1, 185), (1, 1, 183)] (1369701, 1370781) [(3, 1, 183), (3, 1, 185)]
            (1371601, 1372273) [(1, 1, 187), (1, 1, 189)] (1372317, 1371645) [(3, 1, 189), (3, 1, 187)]
            (1373137, 1372777) [(1, 1, 193), (1, 1, 191)] (1372821, 1373181) [(3, 1, 191), (3, 1, 193)]
            (1373376, 1373420) [(1, 1, -195), (3, 1, -195)] (1373448, 1373412) [(3, 3, -195), (1, 3, -195)]
            """
            if self.prev != self.data:
                if self.lead and not self.last:
                    self._edges = {
                        frozenset(self.data[i-1:i+1])
                        for i in range(len(self.data))
                        if self.joined and
                        1 == V[self.data[i-1]][0] == V[self.data[i-1]][1] == V[self.data[i]][0] == V[self.data[i]][1]
                        or not self.joined and
                        3 == V[self.data[i-1]][0] == V[self.data[i]][0] and
                        1 == V[self.data[i-1]][1] == V[self.data[i]][1]
                    }
                else:
                    self._edges = {*map(frozenset, zip(self.data, self.data[1:] + self.data[:1]))}
                self.prev = self.data[:]
            return self._edges

        @property
        def eadjs(self) -> FrozenEdges:
            """
            Edges parallel to and one unit length distance away from each edge in self.edges.

            Calculate only if the data value has changed.
            WITHOUT EA:
            self._eadjs = {
                eadj
                for u, p in map(frozenset, zip(self.data, self.data[1:] + self.data[:1]))
                for eadj in ET & {*map(frozenset, product(A[u] - {p}, A[p] - {u}))}
            }
            """
            if self.data != self.looped:
                self._eadjs = {
                    eadj
                    for edge in map(frozenset, zip(self.data, self.data[1:] + self.data[:1]))
                    for eadj in EA[edge]
                }
                self.looped = self.data[:]
            return self._eadjs

        def join(self, edge=None, oedge=None, other=None):
            """
            Rotates the data according to an edge and extends it to the end.

            Args:
                edge (tuple): the edge to rotate the data to.
                oedge (tuple): the edge to rotate the other data to.
                other (Loop): the other data to join to this one.
            """
            print(
                edge,
                [V[e] for e in edge],
                (oe := oedge if oedge[0] in A[edge[-1]] else oedge[::-1]),
                [V[o] for o in oe]
            )
            self.joined = True
            self.rotate_to_edge(*edge)
            other.rotate_to_edge(*(oedge if oedge[0] in A[edge[-1]] else oedge[::-1]))
            self.data[len(self.data):] = other.data

        def rotate_to_edge(self, start: int, end: int):
            """
            Rotates the data so that the edge matches the ends of the data.

            Edge (1, 7) -> Loop (1, 3, 4, 5, 6, 2, 7)

            Args:
                start (int): the starting vertex of the edge.
                end (int): the ending vertex of the edge.
            """
            if start == self.data[-1] and end == self.data[0]:
                self.data[:] = self.data[::-1]
            elif (ix_start := self.data.index(start)) > (ix_end := self.data.index(end)):
                self.data[:] = self.data[ix_start:] + self.data[:ix_start]
            else:
                self.data[:] = self.data[ix_end - 1::-1] + self.data[:ix_end - 1:-1]

    def weave() -> Solution:
        """
        Warp loom, Weave the weft.
        len of loom is very small:
        for a graph with n vertices:
            n            loops in loom
            79_040   ->  20
            273_760  ->  30
            540_200  ->  37
            762_272  ->  42
        """
        warp, *wefts = warp_loom()
        warp = Loop(warp, lead=True)
        loom = {idx: Loop(weft) for idx, weft in enumerate(wefts)}
        last_idx = len(loom) - 1
        while loom:
            for idx in loom.keys():
                if idx == last_idx:
                    warp.last = True
                if bridge := warp.edges & loom[idx].eadjs:
                    if weft_e := EA[warp_e := bridge.pop()] & loom[idx].edges:
                        warp.join(edge=tuple(warp_e), oedge=tuple(weft_e.pop()), other=loom.pop(idx))
                        break
        return warp.data

    def warp_loom() -> WarpedLoom:
        """
        Spin the yarn, color it. Start at the bottom and work your way up z axis:
        Get all the necessary colored yarn needed for this level to the number of nodes in the current level.
        Wind bobbins.  Take the bobbins and cut the larger colored yarn and wrap the threads around the bobbins.
        Thread the Warp: Join the bobbined yarn to the threads already in the loom.
        Repeat until all the levels are finished.
        Return loom.
        """
        bobbins, loom = None, []
        spool = spin()
        for z, zorder in ZA.items():
            woven = set()
            yarn = [VI[(*xy, z)] for xy in spool[z % 4][-len(zorder) if z == -1 else -zorder:]]
            warps = cut(yarn, bobbins) if bobbins else [yarn]
            for thread in loom:
                for idx, warp in enumerate(warps):
                    if idx not in woven:
                        for end in 0, -1:
                            if thread[end] == warp[0]:
                                woven.add(idx)
                                thread.extend(warp[1:]) if end else thread.extendleft(warp[1:])
            loom.extend((deque(wp) for wp in (w for idx, w in enumerate(warps) if idx not in woven)))
            bobbins = wind(loom) if z != -1 else None
        for w in loom:
            w += [VI[(vector := V[node])[0], vector[1], -vector[2]] for node in reversed(w)]
        return sorted(loom)

    def spin() -> Spool:
        """
        Walk a hamiltonian circuit starting from the node furthest from origin to towards the node closest to origin
        without backtracking by using
        the calculating the attrition factor and ordering the next steps accordingly. When calculating this factor,
        if the start node is either the
        centermost or the outermost node, it can walk all paths without backtracking.

        spin() -> yarn: walk a hamiltonian circuit starting from the node furthest from origin to towards the node
        closest to origin. One should find
        the hamiltonian path from the largest level in order to produce the longest piece of yarm. If the initial
        tour came from the least nodes ie.,
        min(vector[2]) it would result in only a tour with four nodes, which is useless in creating other tours.

        Color the natural thread blue by rotating the sequence vectors 180 degrees around the z-axis and displace 1
        unit length along the y-axis.
        """
        spool = [max(ZA[-1])]
        to_spin = len(ZA[-1]) - 1
        for _ in range(to_spin):
            spool += sorted(ZA[-1][spool[-1]] - {*spool}, key=lambda n: W[n])[-1:]
        return {
            3: (natural := [V[node][:2] for node in spool]),
            1: np.add(np.dot(np.array(natural), [[-1, 0], [0, -1]])[-ZA[-3]:], [0, 2])
        }

    def cut(tour: Path, subset: NodeSet) -> Paths:
        """

        This function takes in two inputs: a list called `tour` and a set called `subset`. It returns a list of lists.
        It sorts the index of the nodes in `tour` that are in `subset` and creates multiple sublists of `tour`
        based on the indices of the `subset` nodes. Finally, it returns a new list that contains each tour in
        `subtours` in reverse order if the first element of the tour is not in `subset`, otherwise the tour is
        returned as is.

        Args:
        tour: List of integers representing the nodes in a tour.
        subset: set of integers representing the nodes in a subset.

        Returns:
        List of list of integers representing the sublists of `tour`

        Restrictions:
        tour: list of integers, len(tour) > 0
        subset: set of integers, subset ⊆ tour, len(subset) > 0

        Given a list S of integers representing a tour and a subset T of S, where S = {s1, s2, ..., sn} and T = {t1,
        t2, ..., tm},
        the function cut(S, T) returns a new list of lists R, where each list in R is a sublist of S and satisfies
        the following conditions:

            For each r in R, r is a sublist of S and is either a subset of T or its complement set (S-T)
            For each r in R, if the first element of r is not in T, then r is in reverse order.
        """
        subtours, prev, last_ix = [], -1, len(tour) - 1
        for e, idx in enumerate(idxs := sorted((tour.index(node) for node in subset))):
            if e == len(idxs) - 1 and idx != last_ix:
                subtours += [tour[prev + 1: idx], tour[idx:]]
            else:
                subtours += [tour[prev + 1:idx + 1]]
                prev = idx
        return [tour if tour[0] in subset else tour[::-1] for tour in subtours if tour]

    def wind(loom: Loom) -> NodeSet:
        """
        returns a set of bobbins. it sets the bobbins for the next level by adding the upper and lower neighbors of
        the first and last element
        of each thread in the loom. The method iterates over the threads in the loom and adds the upper and lower
        neighbors of the first and last element respectively, to the bobbins set and to the ends of the thread.
        """
        bobbins: NodeSet = set()
        for thread in loom:
            thread.appendleft(left := VI[(v1 := V[thread[0]])[0], v1[1], v1[2] + 2])
            thread.append(right := VI[(v2 := V[thread[-1]])[0], v2[1], v2[2] + 2])
            bobbins |= {left, right}
        return bobbins

    return weave()


def main():
    from utils import info, gens, decs, io
    uon_range = 160, 160
    woven, orders, all_times = None, [], []
    woven = None
    for order in gens.uon(*uon_range):
        ord_times = []
        G = io.get_G(order)
        for _ in range(1):
            start = decs.time.time()
            woven = weave_solution(G['A'], G['V'], G['VI'], G['EA'], G['W'], G['ZA'])
            print(woven)
            dur = decs.time.time() - start
            ord_times.append(dur)
        all_times.append(min(ord_times))
        orders.append(order / 1000000)
        # print('NONTURNS:', count_nonturns(woven, A, V), '|', 'AXES:', count_axes(woven, V), len(woven))
        print(f'⭕️ {order:>7} | ⏱️ {all_times[-1]:.7f} | "🩺", {len(woven)}/{order}: {info.id_seq(woven, G["A"])}')
    print(f'orders = {orders}')
    print(f'all_times = {all_times}')


if __name__ == '__main__':
    main()

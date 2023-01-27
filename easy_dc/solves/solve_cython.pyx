import numpy as np

from collections import deque

from easy_dc.make import shrink_adjacency
from easy_dc.defs import *
from easy_dc.utils.info import id_seq
from easy_dc.utils.gens import uon
from easy_dc.utils.decs import profile, time
from easy_dc.utils.io import get_G, save_G


@profile()
def weave_solution(A: AdjDict, V: Verts, VI: IdxMap, EA: EAdj, W: Weights, ZA: GLvls) -> Solution:
    ends: Ends = 0, -1

    class Loop:
        def __init__(self, loop):
            self.loop: Path = list(loop)
            self.looped = None
            self._eadjs = None

        @property
        def edges(self):
            return {*map(frozenset, zip(self.loop, self.loop[1:] + self.loop[:1]))}

        @property
        def eadjs(self) -> FrozenEdges:
            if self.loop != self.looped:
                self._eadjs = {eadj for edge in self.edges for eadj in EA[edge]}
                self.looped = self.loop[:]
            return self._eadjs

        def join(self, edge=None, oedge=None, other=None):
            self.rotate_to_edge(*edge)
            other.rotate_to_edge(*(oedge if oedge[0] in A[edge[-1]] else oedge[::-1]))
            self.loop[len(self.loop):] = other.loop

        def rotate_to_edge(self, start: int, end: int):
            if start == self.loop[-1] and end == self.loop[0]:
                self.loop[:] = self.loop[::-1]
            elif (ix_start := self.loop.index(start)) > (ix_end := self.loop.index(end)):
                self.loop[:] = self.loop[ix_start:] + self.loop[:ix_start]
            else:
                self.loop[:] = self.loop[ix_end - 1::-1] + self.loop[:ix_end - 1:-1]

    def weave() -> Solution:
        warp = (loom := warp_loom()).pop(0)
        while loom:
            for ix_weft in loom.keys():
                if bridge := warp.edges & (weft := loom[ix_weft]).eadjs:
                    if weft_edges := EA[warp_edge := bridge.pop()] & weft.edges:
                        warp.join(edge=tuple(warp_edge), oedge=tuple(weft_edges.pop()), other=loom.pop(ix_weft))
                        break
        return warp.loop

    def warp_loom() -> WarpedLoom:
        bobbins, loom = None, []
        spool = spin()
        for z, zorder in ZA.items():
            woven = set()
            yarn = [VI[(*xy, z)] for xy in spool[z % 4][-len(zorder) if z == -1 else -zorder:]]
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
            bobbins = wind(loom) if z != -1 else None
        for w in loom:
            w += [VI[(vector := V[node])[0], vector[1], -vector[2]] for node in reversed(w)]
        return {idx: Loop(warp) for idx, warp in enumerate(sorted(loom))}

    def spin() -> Spool:
        spool = [max(ZA[-1])]
        rest = len(ZA[-1]) - 1
        for _ in range(rest):
            spool.append(sorted(ZA[-1][spool[-1]] - {*spool}, key=lambda n: W[n])[-1])

        return {
            3: (natural := [V[node][:2] for node in spool]),
            1: np.add(np.dot(np.array(natural), [[-1, 0], [0, -1]])[-ZA[-3]:], [0, 2])
        }

    def cut(tour: Path, subset: NodeSet) -> Paths:
        subtours, prev = [], -1
        last_idx = len(tour) - 1
        ixs = sorted((tour.index(node) for node in subset))
        for e, ix in enumerate(ixs):
            if e == len(ixs) - 1 and ix != last_idx:
                if len(t1 := tour[prev + 1: ix]) > 1 or not t1:
                    subtours += [t1, tour[ix:]]
                else:
                    subtours += [tour[prev + 1: ix + 1]]
            else:
                subtours += [tour[prev + 1:ix + 1]]
                prev = ix
        return [tour if tour[0] in subset else tour[::-1] for tour in subtours if tour]

    def wind(loom: Loom) -> NodeSet:
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
    uon_range = 32, 79040
    woven, orders, all_times = None, [], []
    woven = None
    for order in uon(*uon_range):
        ord_times = []
        G = get_G(order)
        A, V, VI, EA, W = G['A'], G['V'], G['VI'], G['EA'], G['W']
        ZA = G['ZA'] = shrink_adjacency(A, V)
        save_G(G)
        for _ in range(1):
            start = time.time()
            woven = weave_solution(A, V, VI, EA, W, ZA)
            dur = time.time() - start
            # print(f'⏱️ {dur:.7f} ')
            # print('NONTURNS:', count_nonturns(woven, A, V), '|', 'AXES:', count_axes(woven, V), len(woven))
            ord_times.append(dur)
        all_times.append(min(ord_times))
        orders.append(order / 1000000)
        print(f'⭕️ {order:>7} | ⏱️ {all_times[-1]:.7f} | "🩺", {len(woven)}/{order}: {id_seq(woven, G["A"])}')
    print(f'orders = {orders}')
    print(f'all_times = {all_times}')


if __name__ == '__main__':
    main()
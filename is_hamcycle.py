class IsHamCycle:
    """
    A class of minifunctions that tests various theorems against a self.A object to tell, using those theorems if the object is hamiltonian.
    """
    def __init__(self, A):
        self.A = A
        self.ORD = len(self.A)

    def dirac(self):
        """
        A simple self.A with n vertices n ≥ 3 is Hamiltonian if every vertex has degree n / 2 or greater
        """
        for node in self.A:
            if len(self.A[node]) < self.ORD / 2:
                return False
        return True

    def ore(self):
        for n1 in self.A:
            for n2 in self.A:
                if n1 != n2:
                    if n1 not in (n2adj := self.A[n2]):
                        if len(self.A[n1]) + len(n2adj) < self.ORD:
                            return False
        return True

    def bipartite(self):
        # check if the graph is bipartite
        odd_even = {0: {0}, 1: {*self.A[0]}}
        while {*A} - (odd_even[0] | odd_even[1]):
            for odd in odd_even[0]:
                odd_even[1] |= A[odd]
            for even in odd_even[1]:
                odd_even[0] |= A[even]

        # check if the size of the two partitions are equal
        if len(odd_even[0]) != len(odd_even[1]):
            return False

        for i in (0, 1):
            odd, even = odd_even[i], odd_even[abs(i - 1)]
            # check the condition of the theorem for each k in range 1 to n/2
            for k in range(1, self.ORD // 2):
                # for each vertex in partition 1 with degree less than k
                F = {n for n in odd if len(self.A[n]) < k}
                # for each vertex in partition 2 with degree less than n-k
                for e in even:
                    if len(self.A[e]) < self.ORD - k:
                        # check that q is adjacent to at least one vertex in F
                        if not any(f in self.A[e] for f in F):
                            return False


if __name__ == '__main__':
    from easy_dc.utils import *

    order = 32
    G = get_G(order)
    A = G['A']
    ish = IsHamCycle(A)
    res = ish.bipartite()
    print(res)
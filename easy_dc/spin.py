from easy_dc.utils.io import get_G
from easy_dc.make import shrink_adjacency


def spin(A: dict[int, set[int]], V: list[tuple[int, int, int]]) -> list[int]:
    """
    New spin method that doesn't need to sort.
    """

    AA = {}
    start = max(A.keys())
    print(start)
    floors = reversed(range(3, sum(map(abs, V[start])) + 1, 2))
    for floor in floors:
        AA[floor] = {k: {v for v in vals if sum(map(abs, V[v])) >= floor} for k, vals in A.items() if sum(map(abs, V[k])) >= floor}

    print(AA)
    path = [start]
    floors = reversed(range(3, sum(map(abs, V[start])) + 1, 2))
    for floor in floors:
        print('FLOOR:', floor)
        while True:
            print(path)
            if step := AA[floor][path[-1]] - {*path}:
                print(len(step))
                path.append(*step)
            else:
                break


"""
pub fn graph32() -> Adj {
    let graph = hash_map! {
        1 => Neighbors::Six([1, 2, 3, 4, 5, 6]),
        2 => Neighbors::Three([1, 2, 3]),
        3 => Neighbors::Six([1, 2, 3, 4, 5, 6]),
        4 => Neighbors::Three([1, 5, 6]),
    };
    graph
}

"""


def parse_graph(A):
    """
    Print out graph as a rust.rs file...
    """
    order = len(A)
    with open(f"/home/rommelo/Repos/RustRepos/hamcycle/src/graphs/adj{order}.rs", "w") as file:
        lines = [
            "use common_macros::hash_map;\n\nuse crate::types::types::Adj;\nuse crate::enums::enums::Neighbors;\n\n",
            f"pub fn adj{order}() -> Adj {{\n",
            f"    let graph = hash_map! {{\n"
        ]
        lines += [f"        {k} => Neighbors::{'Six' if len(v) == 6 else 'Three'}({sorted(v, key=lambda node: len(A[node]))}),\n" for k, v in A.items()]
        lines += ["    };\n    graph\n}"]
        file.writelines(lines)
    return file


"""
pub const GRAPH: [(u32, &[u32]); 32] = [    
    (0, &[1, 2, 4, 8, 12, 14]),
    (1, &[0, 3, 5, 9, 13, 15]),
    (2, &[0, 3, 6, 10, 16, 18]),
    (3, &[1, 2, 7, 11, 17, 19]),
    (4, &[0, 5, 6, 20, 22, 28]),
    (5, &[1, 4, 7, 21, 23, 29]),
    (6, &[2, 4, 7, 24, 26, 30]),
    (7, &[3, 5, 6, 25, 27, 31]),
    (8, &[0, 9, 10]),
    (9, &[1, 8, 11]),
    (10, &[2, 8, 11]),
    (11, &[3, 9, 10, 3]),
    (12, &[0, 20, 13]),
    (13, &[1, 12, 21]),
    (14, &[0, 16, 22]),
    (15, &[1, 17, 23]),
    (16, &[24, 2, 14]),
    (17, &[25, 3, 15]),
    (18, &[19, 2, 26]),
    (19, &[27, 18, 3]),
    (20, &[21, 4, 12]),
    (21, &[13, 20, 5]),
    (22, &[24, 4, 14]),
    (23, &[25, 5, 15]),
    (24, &[16, 6, 22]),
    (25, &[17, 23, 7]),
    (26, &[18, 27, 6]),
    (27, &[26, 19, 7]),
    (28, &[4, 29, 30]),
    (29, &[28, 5, 31]),
    (30, &[28, 6, 31]),
    (31, &[29, 30, 7]),
];

"""

def print_verts(V):
    print(f"pub const VAR: [[i32; 3]; {len(V)}] = [")
    for i in range(len(V)):
        if i == len(V) - 1:
            print(f"    {list(V[i])}")
        else:
            print(f"    {list(V[i])},")
    print("];")


def parse_const_graph(order):
    """
    Print out graph as a rust.rs file...
    """
    graph = get_G(order)
    A, V, E = graph['A'], graph['V'], graph['E']

    order = len(A)

    with open(f"/home/rommelo/Repos/RustRepos/hamcycle/src/graphs/data/g_{order}.rs", "w") as file:
        lines = [f"pub const VERTS: &[(i32, i32, i32)] = &{list(V)};\n\n"]
        # lines += [f"pub const VAR: [[i32; 3]; {len(V)}] = [\n"]
        lines += [f"pub const VAR: &[[i32; 3]] = [\n"]

        lines += [f"    {list(V[i])}\n" if i == len(V) - 1 else f"    {list(V[i])},\n" for i in range(len(V))]
        lines += [f"];\n\n"]
        lines += [f"pub const ADJ: [(u32, &[u32]); {order}] = [  \n"]
        lines += [f"    ({k}, &{sorted(v, key=lambda node: len(A[node]))}),\n" for k, v in A.items()]
        line = lines.pop()
        lines += [line[:-2], "\n"]
        lines += ["];\n\n"]
        lines += [f"pub const EDGES: &[(u32, u32)] = &{list(map(tuple, E))};\n"]
        file.writelines(lines)
    return file


if __name__ == '__main__':
    from easy_dc.utils.gens import uon

    for order in uon(32, 79040):
        parse_const_graph(order)


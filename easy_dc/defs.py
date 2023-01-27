from typing import (
    Any,
    Dict,
    FrozenSet,
    List,
    Set,
    Tuple,
    Union,
    Deque,
    Optional,
    Iterable,
    Generator,
    Iterator,
)

import numpy as np


class Xy:
    """
    A class for performing mathematical operations on a set of values.

    The class stores a list of values and allows for addition, subtraction,
    multiplication, and division of the values, either with scalars or other
    Xy instances. It also provides a tuple representation of the values and
    allows iteration over the values.

    Attributes:
        values (list): The list of values.

    Examples:
        >>> xyz = Xy([1, 2, 3])
        >>> xyz.values
        [1, 2, 3]
        >>> xyz.data
        (1, 2, 3)
        >>> for value in xyz:
        ...     print(value)
        1
        2
        3
        >>> xyz2 = Xy([4, 5, 6])
        >>> xyz3 = xyz + xyz2
        >>> xyz3.values
        [5, 7, 9]
    """

    def __init__(self, values):
        self.values = values

    @property
    def data(self):
        return tuple(self.values)

    def __iter__(self):
        return iter(self.values)

    def __add__(self, other):
        return Xy([x + y for x, y in zip(self.values, other.values)])

    def __sub__(self, other):
        return Xy([x - y for x, y in zip(self.values, other.values)])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Xy([x * other for x in self.values])
        else:
            return Xy([x * y for x, y in zip(self.values, other.values)])

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Xy([x / other for x in self.values])
        else:
            return Xy([x / y for x, y in zip(self.values, other.values)])

    def __str__(self):
        return str(self.data)


"""
Filepaths to be replaced with nonmanual
"""
FP_GRAPHS = "/mnt/a9f6bede-6105-4049-a22d-aeb740b1e684/graphs_discocube"

"""
TYPE DEFINITIONS
"""

AdjDict = Dict[int, Set[int]]
AdjDictVect = Dict[Tuple[int], Set[Tuple[int]]]
Ends = Tuple[int]
Path = List[int]
Spool = Dict[int, Union[np.ndarray, List[List[int]]]]
Paths = List[Path]
Verts = Tuple[Tuple[int, int, int]]
EAdj = Dict[FrozenSet[int], Set[FrozenSet[int]]]
Edges = Tuple[Tuple[int, int]]
IdxMap = Dict[Any, int]
NodesMap = Dict[int, int]
GLvls = Dict[int, Union[int, Dict[str, Any]]]
NodeSet = Set[int]
Cycle = Tuple[int]
Mapping = Dict[int, int]
QuickSet = Set[Iterable]
Graph = Dict[str, Union[Verts, IdxMap, Edges, AdjDict, EAdj, Mapping]]
NodesGroup = Dict[int, Set[int]]
Warp = Deque[int]
Start = Optional[int]
Weights = Dict[int, Union[int, float]]
Vector = Tuple[int]
UonGen = Generator[int, None, None]
Unpacker = Iterator[int]
AxisVectors = Dict[str, Dict[str, Any]]
BasisVectors = List[Xy]
AxisRotations = Dict[str, Dict[str, Xy]]
Certificate = str or bool
Loom = List[Warp]
WarpedLoom = Dict[int, Any]
Solution = List[int]
FrozenEdges = Set[FrozenSet[int]]
ColoredYarn = Union[List[List[int]], np.ndarray]
Yarn_Spool = Dict[str, ColoredYarn]


__all__ = [
    'AdjDict',
    'AdjDictVect',
    'Any',
    'AxisRotations',
    'AxisVectors',
    'BasisVectors',
    'Certificate',
    'ColoredYarn',
    'Cycle',
    'Edges',
    'EAdj',
    'Ends',
    'FrozenEdges',
    'FP_GRAPHS',
    'Graph',
    'GLvls',
    'IdxMap',
    'Iterable',
    'Loom',
    'Mapping',
    'NodesGroup',
    'NodesMap',
    'NodeSet',
    'Optional',
    'Path',
    'Paths',
    'QuickSet',
    'Solution',
    'Spool',
    'Start',
    'UonGen',
    'Union',
    'Unpacker',
    'Verts',
    'Vector',
    'Warp',
    'WarpedLoom',
    'Weights',
    'Xy',
    'Yarn_Spool'
]

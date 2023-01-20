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
from easy_dc.xyz import Xy

"""
Filepaths to be replaced with nonmanual
"""
FP_GRAPHS = "/mnt/a9f6bede-6105-4049-a22d-aeb740b1e684/dcgraphs"

"""
TYPE DEFINITIONS
"""

AdjDict = Dict[int, Set[int]]
Ends = Tuple[int]
Path = List[int]
Paths = List[Path]
Verts = Tuple[Tuple[int, int, int]]
EAdj = Dict[FrozenSet[int], Set[FrozenSet[int]]]
Edges = Tuple[Tuple[int, int]]
IdxMap = Dict[Any, int]
NodesMap = Dict[int, int]
GLvls = Dict[int, Dict[str, Any]]
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
Solution = List[int]
FrozenEdges = Set[FrozenSet[int]]

__all__ = [
    'AdjDict',
    'Any',
    'AxisRotations',
    'AxisVectors',
    'BasisVectors',
    'Certificate',
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
    'Start',
    'UonGen',
    'Union',
    'Unpacker',
    'Verts',
    'Vector',
    'Warp',
    'Weights',
]

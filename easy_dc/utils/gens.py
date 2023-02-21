from easy_dc.defs import Unpacker, UonGen, Iterable


def unpack(nested_list) -> Unpacker:
    """
    Unpack (completely) a nested list into a generator
    """
    for nested in nested_list:
        if isinstance(nested, Iterable) and not isinstance(nested, (str, bytes)):
            yield from unpack(nested)
        else:
            yield nested


def uon(start=8, end=3000000, max_n=800) -> UonGen:
    """
    Generator for the uncentered octahedral numbers.
    """
    for i in range(max_n + 2):
        _uon = sum([(n * (n + 2)) for n in range(0, max_n * 2 + 2, 2)][:i])
        if end >= _uon >= start:
            yield _uon

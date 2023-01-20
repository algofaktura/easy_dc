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

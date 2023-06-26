from chess.constants import LETTERS, NUMBERS


def algebraic_to_index(an):
    """
    Converts from algebraic notation to an index
    :param an: str
    :return: int
    """
    c = LETTERS.index(an[0])
    r = NUMBERS[::-1].index(an[1])
    return 8 * r + c


def index_to_algebraic(i):
    """
    Converts from an index to algebraic notation
    :param i: int
    :return: str
    """
    c, r = index_to_coordinate(i)
    return LETTERS[c] + NUMBERS[::-1][r]


def index_to_coordinate(i):
    """
    Converts from an index to a (col, row) coordinate
    :param i: int
    :return: (int, int)
    """
    return i % 8, i // 8


def coordinate_to_index(square):
    """
    Converts from a (col, row) coordinate to an index
    :param square: (int, int)
    :return: int
    """
    c, r = square
    return c + r * 8

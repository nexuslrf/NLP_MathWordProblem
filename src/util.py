import enum


class Operators(enum.Enum):
    equal = 0
    plus = 1
    minus = 2
    times = 3
    divide = 4


def reverse(s):
    return s[::-1]
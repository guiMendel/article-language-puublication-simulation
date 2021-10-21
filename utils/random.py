from random import randrange, random


def skewed_range(init, end, skew):
    """Returns a number in the range, skewed to the center by skew amount"""
    return sum([randrange(init, end) for _ in range(skew)]) / skew


def skewed_random(skew):
    """Returns a number in [0, 1), skewed to the center by skew amount"""
    return sum([random() for _ in range(skew)]) / skew

from random import randrange, random


def skewed_range(init, end, skew, round_result=False):
    """Returns a number in the range, skewed to the center by skew amount"""
    result = sum([randrange(init, end) for _ in range(skew)]) / skew
    return round(result) if round_result else result


def skewed_random(skew):
    """Returns a number in [0, 1), skewed to the center by skew amount"""
    return sum([random() for _ in range(skew)]) / skew

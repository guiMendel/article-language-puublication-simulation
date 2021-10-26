from random import randrange, random, sample
from typing import Iterable
import numpy as np


def skewed_range(init, end, skew, round_result=False):
    """Returns a number in the range, skewed to the center by skew amount"""
    result = sum([randrange(init, end) for _ in range(skew)]) / skew
    return round(result) if round_result else result


def skewed_random(skew):
    """Returns a number in [0, 1), skewed to the center by skew amount"""
    return sum([random() for _ in range(skew)]) / skew


def weighted_sample(
    iterable: Iterable, weights: list[float], sample_size: int, replace=True
):
    # If weights are 0, return randomly
    if sum(weights) == 0:
        return sample(iterable, sample_size)

    # In case items do not sum to 1, we need to tweak them:

    # How much we need to multiply each weight by
    weights_correction = 1.0 / sum(weights)

    # Apply the correction
    weights_corrected = np.array(weights) * weights_correction

    return np.random.choice(
        iterable,
        sample_size,
        replace,
        weights_corrected,
    ).tolist()

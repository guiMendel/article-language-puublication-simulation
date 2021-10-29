from typing import Callable
from data.list_of_names import list_of_names
import numpy as np
import random

# config
import tuning

# ID number generator
def id_getter() -> Callable[[], int]:
    # IDs taken
    ids_taken = 0

    def get() -> int:
        nonlocal ids_taken
        ids_taken += 1

        return ids_taken - 1

    return get


# Author name generator
def generate_author_name() -> str:
    names = random.sample(list_of_names, 2)
    return " ".join(names)


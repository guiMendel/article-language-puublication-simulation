from data.list_of_names import list_of_names
from data.language_frequency import language_frequency
import numpy as np
import random

# config
from tuning import chance_of_extra_language

# Author name generator
def generate_author_name():
    names = random.sample(list_of_names, 2)
    return " ".join(names)


# Language proficiency list generation
def generate_language_proficiency_list():
    # The language frequencies do not sum to 1, so we need to tweak them:
    # The frequencies
    frequencies = list(language_frequency.values())

    # How much we need to multiply each frequency by
    frequencies_correction = 1.0 / sum(frequencies)

    # Apply the correction
    frequencies_corrected = np.array(frequencies) * frequencies_correction

    # Decide how many languages will be added to the list
    language_count = 1
    while random.random() <= chance_of_extra_language:
        language_count += 1

    return np.random.choice(
        list(language_frequency.keys()), language_count, False, frequencies_corrected
    ).tolist()

# Journal name generator

# Article name generator

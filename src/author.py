import random
from mesa import Agent

from utils.generators import generate_author_name, generate_language_proficiency_list
from utils.random import skewed_random, skewed_range
from tuning import author_lifespan_range, author_lifespan_skew


class Authors(Agent):
    """A author agent"""

    # Initialize author
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Generate a competency, skewed to the medium
        self.competency = skewed_random(5)

        # Generate a name
        self.name = generate_author_name()

        # Generate language proficiency list
        self.languages = generate_language_proficiency_list()

        # Get lifespan
        self.months_left = round(
            skewed_range(
                author_lifespan_range[0], author_lifespan_range[1], author_lifespan_skew
            )
        )

    def step(self):
        pass

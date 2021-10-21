import random
from mesa import Agent

from utils.generators import generate_author_name


class Researcher(Agent):
    """A researcher agent"""

    # Initialize researcher
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Generate a competency, skewed to the medium
        self.competency = sum([random.random() for _ in range(5)]) / 5.0

        # Generate a name
        self.name = generate_author_name()

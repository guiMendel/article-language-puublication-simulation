from mesa import Agent

from utils.generators import generate_author_name, generate_language_proficiency_list
from utils.random import skewed_random, skewed_range

from tuning import (
    author_lifespan_range,
    author_lifespan_skew,
)


class Author(Agent):
    """An author agent"""

    # Initialize author
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Generate a competency, skewed to the medium
        self.competency = skewed_random(5)

        # Generate a name
        self.name = generate_author_name()

        # Generate language proficiency list
        self.languages = generate_language_proficiency_list()

        # Will hold reference to whichever article it's currently working
        self.working_on = None

        # Get lifespan
        self.articles_left = skewed_range(
            author_lifespan_range[0],
            author_lifespan_range[1],
            author_lifespan_skew,
            True,
        )

    def step(self):
        # print(
        #     f"I am {self.name}, author number {self.unique_id}. I speak {', '.join(self.languages)}, and I am {'average smart' if self.competency <= 0.7 else 'AMAZINGLY smart' }.  I will publish {self.articles_left} articles."
        # )

        # Check if is retired
        if self.articles_left == 0:
            return

        # Check if it is busy. If not, start new article
        if self.working_on is None:
            # Count new article
            self.articles_left -= 1

            # Check if done
            if self.articles_left > 0:
                # Apply for an article creation
                self.model.apply_for_article(self)

            else:
                self.model.retire(self)

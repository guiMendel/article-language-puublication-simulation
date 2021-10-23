from typing import Tuple
from mesa import Agent, Model
from src.author import Author
from utils.months import Month
from utils.random import skewed_random, skewed_range

from tuning import (
    article_cost_range,
    article_cost_skew,
)


class Article(Agent):
    """Defines an article"""

    def __init__(
        self,
        unique_id: int,
        model: Model,
        name: str,
        authors: list[Author],
        language: str,
    ):
        # Call super
        super().__init__(unique_id, model)

        self.name = name
        self.authors = authors
        self.language = language
        self.publish_date: Tuple[Month, int] = None

        # Get article time cost
        self.cost = skewed_range(
            article_cost_range[0],
            article_cost_range[1],
            article_cost_skew,
            True,
        )

    def step(self):
        # Do nothing if already published
        if self.publish_date:
            return

        self.cost -= 1

        # Check if complete
        if self.cost <= 0:
            # Add to completed articles
            self.model.publish(self)

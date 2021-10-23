from typing import Tuple
from mesa import Agent, Model
from numpy.lib.function_base import average
from src.author import Author
from utils.months import Month
from utils.random import skewed_range, weighted_sample

import tuning


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
        self.referencing_articles: list[Article] = []
        self.publish_date: Tuple[Month, int] = None

        # Get article time cost
        self.cost = skewed_range(
            tuning.article_cost_range[0],
            tuning.article_cost_range[1],
            tuning.article_cost_skew,
            True,
        )

        # Define references
        self.define_references()

        # Get article quality
        self.quality = (1 - tuning.article_quality_randomness) * average(
            [author.competency for author in self.authors]
        ) + tuning.article_quality_randomness * self.random.random()

    def step(self):
        # Do nothing if already published
        if self.publish_date:
            return

        self.cost -= 1

        # Check if complete
        if self.cost <= 0:
            # Add to completed articles
            self.model.publish(self)

    def define_references(self):
        self.references: list[Article] = []

        # Get all articles that can be referenced
        accessible_articles = self.get_accessible_articles()

        # Find out how many
        reference_count = 1
        while self.random.random() <= tuning.reference_chance:
            reference_count += 1

        # Ensure there's enough articles for this
        if reference_count > len(accessible_articles):
            reference_count = len(accessible_articles)

        # Don't try to sample if there are none
        if reference_count > 0:
            self.references = weighted_sample(
                accessible_articles,
                weights=[
                    article_attractiveness(article) for article in accessible_articles
                ],
                sample_size=reference_count,
            )

    def get_age(self):
        return self.model.year - self.publish_date[1]

    def get_accessible_articles(self) -> list:
        # Get author language pool
        language_pool: set[str] = set()
        for author in self.authors:
            language_pool.update(author.languages)

        # Get all articles with a language in the pool
        accessible_articles: list[Article] = [
            article
            for article in self.model.published_articles
            if article.language in language_pool
        ]

        # Add subset of globally accessible articles
        accessible_range = round(
            len(self.model.published_articles) * self.model.access_level
        )

        accessible_articles += self.model.published_articles[:accessible_range]

        return accessible_articles


def article_attractiveness(article: Article):
    # Apply quality/reference count
    attractiveness = len(
        article.referencing_articles
    ) * tuning.reference_count_attractability + article.quality * (
        1 - tuning.reference_count_attractability
    )

    # Apply age factor
    attractiveness *= tuning.reference_age_unattractiveness ** article.get_age()

    return attractiveness

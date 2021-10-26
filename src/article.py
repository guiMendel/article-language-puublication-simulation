from pprint import pprint
from typing import Tuple
from mesa import Agent, Model
import numpy as np
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
        accessible_articles: list[Article] = self.get_accessible_articles()

        # Find out how many
        reference_count = (
            round(
                skewed_range(
                    tuning.reference_count_range[0],
                    tuning.reference_count_range[1],
                    tuning.reference_count_skew,
                    True,
                )
                # Smooth out reference count on the first years
                * tuning.reference_chance_modifier(len(self.model.published_articles))
            )
            if len(self.model.published_articles) > 0
            else 0
        )

        # Ensure there's enough articles for this
        if reference_count > len(accessible_articles):
            reference_count = len(accessible_articles)

        # Find out how many samples will be random
        random_sample_count = round(tuning.reference_randomly_chance * reference_count)

        # Get random samples
        self.references = self.random.sample(accessible_articles, random_sample_count)

        # Get weighted sampling pool
        accessible_articles = accessible_articles[: tuning.reference_sampling_pool_size]

        # Don't try to sample if there are none
        if reference_count - random_sample_count > 0:
            self.references += weighted_sample(
                accessible_articles,
                weights=[
                    article.get_attractiveness() for article in accessible_articles
                ],
                sample_size=reference_count - random_sample_count,
            )

        # Count references
        if not self.model.yearly_references.get(self.model.year):
            self.model.yearly_references[self.model.year] = {}

        for reference in self.references:
            if not self.model.yearly_references[self.model.year].get(
                reference.publish_date[1]
            ):
                self.model.yearly_references[self.model.year][
                    reference.publish_date[1]
                ] = 1
            else:
                self.model.yearly_references[self.model.year][
                    reference.publish_date[1]
                ] += 1

    def get_age(self):
        if self.model.year == self.publish_date[1]:
            return 0

        # Get year difference
        year_difference = self.model.year - self.publish_date[1]

        # Get month difference
        month_distance = self.publish_date[0].value + (12 - self.model.month.value)

        # Return final difference
        return year_difference - 1 + (1 if month_distance >= 12 else 0)

    def get_accessible_articles(self) -> list:
        return self.model.published_articles

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

        # Sort them
        accessible_articles = sorted(
            accessible_articles,
            reverse=True,
            key=lambda article: article.get_attractiveness(),
        )

        return accessible_articles

    def get_attractiveness(self):
        # Find out proportion between referencing_articles / global max number of referencing_articles
        reference_count_ratio = (
            (len(self.referencing_articles) / self.model.max_referencing_articles)
            if self.model.max_referencing_articles > 0
            else 0
        )

        # Apply quality/reference count
        attractiveness = (
            reference_count_ratio * tuning.reference_count_attractability
            + self.quality * (1 - tuning.reference_count_attractability)
        )

        # Apply age factor
        attractiveness *= tuning.reference_age_unattractiveness ** self.get_age()

        return attractiveness

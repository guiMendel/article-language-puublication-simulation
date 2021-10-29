from mesa import Agent

from utils.generators import generate_author_name
from utils.random import skewed_random, skewed_range, weighted_sample

import tuning
import numpy as np


class Author(Agent):
    """An author agent"""

    # Initialize author
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Generate a competency, skewed to the medium
        self.competency = skewed_random(tuning.author_competency_skew)

        # Generate a name
        self.name = generate_author_name()

        # Generate language proficiency list
        self.languages = self.generate_language_proficiency_list()

        # Will hold reference to whichever article it's currently working
        self.working_on = None

        # What language is currently being learned, and for how long
        self.learning_language = None
        self.learning_language_months_left = 0

        # Get lifespan
        self.articles_left = skewed_range(
            tuning.author_lifespan_range[0],
            tuning.author_lifespan_range[1],
            tuning.author_lifespan_skew,
            True,
        )

        # print(f'{self.name} speaks {", ".join(self.languages)}')

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

                self.learn_languages()

            else:
                self.model.retire(self)

        else:
            self.learn_languages()

    def generate_language_proficiency_list(self):
        # Decide how many languages will be added to the list
        language_count = 1
        while self.random.random() <= tuning.chance_of_extra_language:
            language_count += 1

        return set(
            weighted_sample(
                list(self.model.language_weights.keys()),
                list(self.model.language_weights.values()),
                language_count,
            )
        )

    def learn_languages(self):
        # If already learning one, discount a month
        if self.learning_language:
            self.learning_language_months_left -= 1

            # If done, add language to languages
            if self.learning_language_months_left <= 0:
                # print(f"{self.name} just learned {self.learning_language}!")

                self.languages.add(self.learning_language)
                self.learning_language = None

            return

        # If not yet learning something, apply chance to begin
        if self.random.random() > tuning.begin_learning_language_chance:
            return

        # Chance to learn english regardless of top articles
        if (
            "English" not in self.languages
            and self.random.random() <= tuning.language_learning_english_bias
        ):
            self.start_learning("English")
            return

        # Start learning something new
        language_sampling_pool: list[str] = []

        # Check top languages
        for article in self.model.published_articles:
            # Check if author already knows this language
            if article.language in self.languages:
                continue

            # Add to pool
            language_sampling_pool.append(article.language)

            # Check if done
            if len(language_sampling_pool) >= tuning.language_sampling_pool_size:
                break

        # If no languages available, too bad!
        if len(language_sampling_pool) == 0:
            return

        # Sample a language from one of these top languages
        self.start_learning(self.random.choice(language_sampling_pool))

    def start_learning(self, language: str):
        self.learning_language = language

        # Set how long it will take to learn language
        self.learning_language_months_left = skewed_range(
            tuning.language_learning_duration_range[0],
            tuning.language_learning_duration_range[1],
            tuning.language_learning_duration_skew,
            True,
        )

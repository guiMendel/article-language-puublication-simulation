from pprint import pprint
from src.article import Article
from src.author import Author
from utils.article_name_generator import generate_article_name
from utils.months import Month
from utils.random import skewed_range, weighted_sample
from utils.generators import id_getter
from mesa import Model
from mesa.time import RandomActivation
import tuning

# Initialize id getter
get_id = id_getter()


class ArticlesModel(Model):
    """A model with some number of agents"""

    def __init__(self, author_count: int) -> None:

        # === Attributes
        self.author_count = 0
        self.active_author_count = 0
        self.published_articles: list[Article] = []
        self.access_level = tuning.starting_access_level
        self.yearly_references = {}

        # The number of citations of the article that has the most
        self.max_referencing_articles = 0

        # List of authors waiting for a new article
        self.new_article_waiting_list: list[Author] = []

        # Scheduler
        self.schedule = RandomActivation(self)

        self.introduce_authors(author_count)

    # Monthly action
    def step(self, year: int, month: Month) -> None:
        """Advance the model by one step"""
        # Update date
        self.year = year
        self.month = month

        # Sort articles by reference count
        self.published_articles = sorted(
            self.published_articles,
            reverse=True,
            key=lambda article: article.get_attractiveness(),
        )

        faulty_articles = [
            article
            for article in self.published_articles[
                : tuning.reference_sampling_pool_size
            ]
            if article.publish_date[1] != self.year
        ]

        # if self.year > 1985 and len(faulty_articles) > 0:
        #     pprint(
        #         [
        #             (article.publish_date[1], article.get_attractiveness())
        #             for article in faulty_articles
        #         ]
        #     )

        # Step agents
        self.schedule.step()

        # Introduce new authors
        self.introduce_authors()

        # Create new article projects for authors in waiting list
        self.create_new_articles()

        # Empty waiting list
        self.new_article_waiting_list = []

        # Increment access level
        self.access_level += tuning.yearly_access_level_increment

    def apply_for_article(self, author: Author):
        """Registers the author in a waiting list for new article project distributions"""
        self.new_article_waiting_list.append(author)

    def publish(self, article: Article) -> None:
        """Publish the provided article"""
        article.publish_date = (self.month, self.year)

        # Add it to published list
        self.published_articles.append(article)

        # Set it's authors as idle
        for author in article.authors:
            author.working_on = None

        # Register references
        for reference in article.references:
            reference.referencing_articles.append(article)

            # Keep the max number updated
            if len(reference.referencing_articles) > self.max_referencing_articles:
                self.max_referencing_articles = len(reference.referencing_articles)

        # Remove from scheduler
        self.schedule.remove(article)

    def retire(self, author: Author):
        # Remove from scheduler
        self.schedule.remove(author)

        self.active_author_count -= 1

    def create_new_articles(self):
        """Creates articles for all authors in the waiting list"""
        # Each iteration assembles a whole author team
        while len(self.new_article_waiting_list) > 0:
            # Draw a random author
            author_team = [self.random.choice(self.new_article_waiting_list)]

            # Initialize language pool
            language_pool = author_team[0].languages

            # Add new authors to the team
            extra_author_chance = tuning.extra_author_chance

            while self.random.random() <= extra_author_chance:
                # Apply chance decay
                extra_author_chance -= tuning.extra_author_chance_decay

                # Try to draw an author that speaks at least one of the languages in the pool
                extra_author = self.choose_author_that_speaks(
                    language_pool, exclude=author_team
                )

                # If no authors match the language pool, stop
                if extra_author is None:
                    break

                # Add author
                author_team.append(extra_author)

                # Update language pool
                language_pool.update(extra_author.languages)

            # Having a team and a language pool, we just need to create the article
            self.start_article(
                author_team, self.pick_best_language(list(language_pool))
            )

            # Remove these authors from the waiting list
            for author in author_team:
                self.new_article_waiting_list.remove(author)

    def pick_best_language(self, language_pool: list[str]):
        """Among the provided languages, pick the one expected to reach more people"""
        # Will hold the weights for each language
        language_weights = [0 for _ in language_pool]

        # Go through the top articles
        for article in self.published_articles[: tuning.language_evaluation_pool_size]:
            try:
                language_index = language_pool.index(article.language)
                language_weights[language_index] += 1
            except ValueError:
                continue

        # If no language received a weight, pick randomly
        if sum(language_weights) == 0:
            return self.random.choice(language_pool)

        # Pick based on weight
        return weighted_sample(language_pool, language_weights, 1)[0]

    def choose_author_that_speaks(
        self, language_pool: list[str], exclude: list[Author]
    ):
        return next(
            (
                # Get author
                author
                # From waiting list
                for author in self.new_article_waiting_list
                # As long as at least one of his spoken languages is present in the provided pool
                if any(
                    author_language
                    for author_language in author.languages
                    if author_language in language_pool
                )
                and author not in exclude
                # And isn't excluded
            ),
            # If none match, return None
            None,
        )

    def start_article(self, authors: list[Author], language: str):
        # Define article to be created
        article = Article(
            # Article agent id
            get_id(),
            # Simulation model
            self,
            # Article name
            generate_article_name(),
            # Authors
            authors,
            # Article language
            language,
        )

        # Add article to scheduler
        self.schedule.add(article)

        # print("starting" + article.name)

        # Set authors as working on this article
        for author in authors:
            author.working_on = article

        return article

    def introduce_authors(self, count: int = None):
        generate_count = (
            count
            if count
            else skewed_range(
                tuning.new_author_range[0],
                tuning.new_author_range[1],
                tuning.new_author_skew,
                True,
            )
        )

        for _ in range(generate_count):
            author = Author(get_id(), self)

            # Count author
            self.author_count += 1
            self.active_author_count += 1

            # Add author to scheduler
            self.schedule.add(author)

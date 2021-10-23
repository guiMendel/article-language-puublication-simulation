from src.article import Article
from src.author import Author
from utils.article_name_generator import generate_article_name
from utils.months import Month
from utils.random import skewed_range
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
        self.author_count = author_count
        self.published_articles: list[Article] = []

        # List of authors waiting for a new article
        self.new_article_waiting_list: list[Author] = []

        # Scheduler
        self.schedule = RandomActivation(self)

    # Monthly action
    def step(self, year: int, month: Month) -> None:
        """Advance the model by one step"""
        # Update date
        self.year = year
        self.month = month

        # Introduce new authors
        self.introduce_monthly_authors()

        # Step agents
        self.schedule.step()

        # Create new article projects for authors in waiting list
        self.create_new_articles()

        # Empty waiting list
        self.new_article_waiting_list = []

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

        # Remove from scheduler
        self.schedule.remove(article)

    def retire(self, author: Author):
        # Remove from scheduler
        self.schedule.remove(author)

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
            self.start_article(author_team, self.random.choice(list(language_pool)))

            # Remove these authors from the waiting list
            for author in self.new_article_waiting_list:
                self.new_article_waiting_list.remove(author)

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

    def introduce_monthly_authors(self):
        for _ in range(
            skewed_range(
                tuning.new_author_range[0],
                tuning.new_author_range[1],
                tuning.new_author_skew,
                True,
            )
        ):
            author = Author(get_id(), self)

            # Add author to scheduler
            self.schedule.add(author)

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

        # Step all agents
        self.schedule.step()

        # Create new article projects for authors in waiting list
        for author in self.new_article_waiting_list:
            # Define article to be created
            author.working_on = Article(
                # Article agent id
                get_id(),
                # Simulation model
                self,
                # Article name
                generate_article_name(),
                # Author name
                author,
                # Article language
                self.random.choice(author.languages),
            )

            # Add article to scheduler
            self.schedule.add(author.working_on)

        # Empty waiting list
        self.new_article_waiting_list = []

    def apply_for_article(self, author: Author):
        """Registers the author in a waiting list for new article project distributions"""
        self.new_article_waiting_list.append(author)

    def publish(self, article: Article) -> None:
        """Publish the provided article"""
        article.publish_date = (self.month, self.year)

        # Add it
        self.published_articles.append(article)

        # Set it's author as idle
        article.author.working_on = None

        # Remove from scheduler
        self.schedule.remove(article)

    def retire(self, author: Author):
        # Remove from scheduler
        self.schedule.remove(author)

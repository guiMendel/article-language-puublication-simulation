from src.article import Article
from src.author import Author
from utils.months import Month
from mesa import Model
from mesa.time import RandomActivation


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

        # === Initialization

        # Create agents
        for index in range(self.author_count):
            author = Author(index, self)

            # Add to scheduler
            self.schedule.add(author)

    # Monthly action
    def step(self, year: int, month: Month) -> None:
        """Advance the model by one step"""
        # Update date
        self.year = year
        self.month = month

        # Step all agents
        self.schedule.step()

        # Create new article projects for authors in waiting list
        for author in self.new_article_waiting_list:
            # Define article to be created
            author.working_on = Article(
                # Article agent id
                self.schedule.get_agent_count(),
                # Simulation model
                self,
                # Article name
                "thang",
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

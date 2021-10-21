from src.author import Authors
from mesa import Model
from mesa.time import RandomActivation

class ArticlesModel(Model):
    """A model with some number of agents"""

    def __init__(self, author_count):

        # Attributes
        self.author_count = author_count

        # Scheduler
        self.schedule = RandomActivation(self)

        # Create agents
        for index in range(self.author_count):
            author = Authors(index, self)

            # Add to scheduler
            self.schedule.add(author)

    # Monthly action
    def step(self, year, month):
        """Advance the model by one step"""
        # Update date
        self.year = year
        self.month = month

        self.schedule.step()

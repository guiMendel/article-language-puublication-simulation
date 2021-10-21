from src.researcher import Researcher
from mesa import Model


class ArticlesModel(Model):
    """A model with some number of agents"""

    def __init__(self, researcher_count):
        self.researcher_count = researcher_count

        # Create agents
        for index in range(self.researcher_count):
            researcher = Researcher(index, self)

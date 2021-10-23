import data.article_names as article
import random

# config
import tuning


def _pick_word(word_type: str) -> str:
    return random.choice(getattr(article, word_type))


def generate_article_name() -> str:
    # Random chance of picking a layout
    layout_index = round(random.random() * 100)

    if layout_index < len(article.layout):
        layout = article.layout[layout_index]

        # Expand nouns for each if it's placeholdsers
        article_name = _fill_placeholders(layout)

    # Generate without a layout
    else:
        article_name = _expand_article_noun()

    # Capitalize
    if random.random() <= article.all_capitalized_chance:
        article_name = " ".join([word.capitalize() for word in article_name.split(" ")])
    else:
        article_name = article_name.capitalize()


def _fill_placeholders(text: str) -> str:
    # Expand nouns for each placeholder
    return text.format(*[_expand_article_noun() for _ in range(text.count("{}"))])


def _expand_article_noun() -> str:
    # Chance to return connector
    if random.random() <= tuning.connector_chance:
        return _fill_placeholders("{} " + _pick_word("connector") + " {}")

    # Return noun
    return _generate_article_noun(adjective_allowed=True)


def _generate_article_noun(adjective_allowed: bool) -> str:
    # Chance of adjective
    if adjective_allowed and random.random() <= tuning.adjective_chance:
        return f"{_pick_word('adjective')} {_generate_article_noun(adjective_allowed=True)}"

    # Chance of noun as adjective
    if random.random() <= tuning.noun_as_adjective_chance:
        return f"{_pick_word('noun')} {_generate_article_noun(adjective_allowed=False)}"

    # Just return the noun
    return _pick_word("noun")

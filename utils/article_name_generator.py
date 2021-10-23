import data.article_names as article
import random

# config
import tuning


def generate_article_name() -> str:
    # List of unused connectors
    unused_connectors = article.connector.copy()

    # Random chance of picking a layout
    layout_index = round(random.random() * 100)

    if layout_index < len(article.layout):
        layout = article.layout[layout_index]

        # Expand nouns for each if it's placeholdsers
        article_name = _fill_placeholders(layout, unused_connectors)

    # Generate without a layout
    else:
        article_name = _expand_article_noun(unused_connectors)

    # Parse raw noun articles
    article_name = _parse_noun_articles(article_name)

    # Capitalize
    if random.random() <= tuning.all_capitalized_chance:
        article_name = " ".join([_capitalize(word) for word in article_name.split(" ")])
    else:
        article_name = _capitalize(article_name)

    # Make sure it's size is valid
    if not tuning.min_name_size < len(article_name) < tuning.max_name_size:
        # Try again
        return generate_article_name()

    return article_name


def _capitalize(text: str) -> str:
    # Built in capitalize lowers other letters for some reason
    return text[0].upper() + text[1:] if len(text) > 1 else text.upper()


def _parse_noun_articles(text: str) -> str:
    words = text.split(" ")

    try:
        while True:
            # Get next occurrence of <a>
            occurrence = words.index("<a>")

            # Check if word right next to it starts with vowel
            if _is_vowel(words[occurrence + 1][0]):
                words[occurrence] = "an"
            else:
                words[occurrence] = "a"

    except ValueError:
        # No more raw articles!
        pass

    return " ".join(words)


def _is_vowel(letter: str) -> bool:
    return letter in ("a", "e", "i", "o", "u")


def _plurify(word: str) -> str:
    """Returns the word in plural form"""
    # Edge cases
    edge_case = {
        "cactus": "cacti",
        "campus": "campi",
        "child": "children",
        "goose": "geese",
        "man": "men",
        "woman": "women",
        "tooth": "teeth",
        "foot": "feet",
        "mouse": "mice",
        "person": "people",
        "matrix": "matrices",
        "index": "indices",
        "criterion": "criteria",
        "phenomenon": "phenomena",
        # Invariables
        "ash": "ash",
        "fish": "fish",
        "sheep": "sheep",
        "series": "series",
        "species": "species",
        "deer": "deer",
    }

    # If a singular noun ends in ‑y and the letter before the -y is a consonant
    if word.endswith("y") and not _is_vowel(word[-2]):
        return word[:-1] + "ies"

    # If the noun ends with ‑f or ‑fe
    if word.endswith("f") or word.endswith("fe"):
        return (word[:-1] if word.endswith("f") else word[:-2]) + "ves"

    # If the singular noun ends in ‑is
    if word.endswith("is"):
        return word[:-2] + "es"

    # If the singular noun ends in ‑s, -ss, -sh, -ch, -x, -o, or -z
    if (
        (
            word.endswith("s")
            or word.endswith("ss")
            or word.endswith("sh")
            or word.endswith("ch")
            or word.endswith("x")
            or word.endswith("o")
            or word.endswith("z")
        )
        # Exceptions
        and word not in ("photo", "halo", "piano")
    ):
        return word + "es"

    # Edge cases
    if word in edge_case:
        return edge_case[word]

    # Regular case
    return word + "s"


def _pick_word(word_type: str, plural: bool = False) -> str:
    word = random.choice(getattr(article, word_type))

    # If plural, modify word
    if plural:
        return _plurify(word)
    return word


def _fill_placeholders(text: str, unused_connectors: list[str]) -> str:
    # Expand nouns for each placeholder
    return text.format(
        *[_expand_article_noun(unused_connectors) for _ in range(text.count("{}"))]
    )


def _expand_article_noun(unused_connectors: list[str]) -> str:
    # Chance to return connector
    if len(unused_connectors) > 0 and random.random() <= tuning.connector_chance:
        connector = random.choice(unused_connectors)
        # Remove connector
        unused_connectors.remove(connector)

        return _fill_placeholders("{} " + connector + " {}", unused_connectors)

    # Return noun
    return _generate_article_noun(
        plural=random.random() <= tuning.plural_chance,
        adjective_allowed=True,
        article_allowed=True,
    )


def _generate_article_noun(
    plural: bool, adjective_allowed: bool, article_allowed: bool = False
) -> str:
    # Chance of article
    if article_allowed and random.random() <= tuning.noun_article_chance:
        return f"{_place_article(plural)} {_generate_article_noun(plural, adjective_allowed=adjective_allowed)}"

    # Chance of adjective
    if adjective_allowed and random.random() <= tuning.adjective_chance:
        return f"{_pick_word('adjective')} {_generate_article_noun(plural, adjective_allowed=True)}"

    # Chance of noun as adjective
    if random.random() <= tuning.noun_as_adjective_chance:
        return f"{_pick_word('noun')} {_generate_article_noun(plural, adjective_allowed=False)}"

    # Just return the noun
    return _pick_word("noun", plural)


def _place_article(plural: bool) -> str:
    # If plural, always use 'the'
    if plural or random.random() <= 0.5:
        return "the"
    return "<a>"

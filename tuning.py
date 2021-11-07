import math

# === Model settings

# Range of years model should simulate
model_years_range = (1915, 2020)

# === Article publication

# Range of months needed for making an article
article_cost_range = (6, 48)

# Skew of months needed for making an article
article_cost_skew = 3

# Chance of there being another author working on the new article
extra_author_chance = 0.90

# For every extra author, chance decays by this amount
extra_author_chance_decay = 0.15

# Degree of randomness in articles' quality
article_quality_randomness = 0.4

# === Article Referencing

# Chance of referencing an extra article
reference_count_range = (10, 50)
reference_count_skew = 2

# Modifier of the extra article chance, based on the current amount of published articles
# This is important to make the simulation smoother on the first years
reference_chance_modifier = lambda articles_count: articles_count / (
    articles_count + 1000.0
)

# Degree to which reference count affects attractability of article on references
reference_count_attractability = 0.3

# Factor applied to article attractiveness by each year that passes by
reference_age_unattractiveness = 0.95

# How many articles to pick from the top published articles to form the sampling pool
reference_sampling_pool_size = 300

# Fraction of references to be sampled completely randomly (without regard to weight)
reference_randomly_chance = 0.2

# === Article name generation

# Chance of generating a connector for a noun
connector_chance = 0.40

# Chance of generating an adjective for a noun
adjective_chance = 0.5

# Chance of generating and adjective using names from the noun list, for a noun
# Only triggers once finished generating regular adjectives
noun_as_adjective_chance = 0.15

# Chance of all words being capitalized, for some reason
all_capitalized_chance = 0.1

# Chance of a noun being in plural
plural_chance = 0.4

# Chance of a noun having an article, i.e. 'the' or 'a'
noun_article_chance = 0.4

# Minimum name size
min_name_size = 30

# Maximum name size
max_name_size = 200

# === Authors

# Number of initial author
initial_author_count = 300

# Range of new authors per month
new_author_range = (1, 15)

# How much the new authors count gets skewed to the centers
new_author_skew = 1

# Range of articles published per author
author_lifespan_range = (1, 15)

# How much the author's lifespan gets skewed to the center
author_lifespan_skew = 2

# Chance of generating an extra language in each iteration
chance_of_extra_language = 0.35

# How much authors competencies tend to be pushed to 0.5
author_competency_skew = 4

# === Language Learning & Choosing

# How many articles from the top referenced list will serve as a sampling pool
language_sampling_pool_size = 10

# Chance of starting to learn a new language each month (that's not already spent learning a language)
begin_learning_language_chance = 0.10

# Range of months it takes to learn a new language
language_learning_duration_range = (18, 42)
language_learning_duration_skew = 2

# Chance of choosing english regardless of top articles
language_learning_english_bias = 0.8

# Number of articles to look up for determining the language weights when picking an article's language
article_language_evaluation_pool_size = 100

# Number of articles to look up when updating the model's language weights
language_evaluation_pool_size = 1000

# How much of an impact do each month's language weights have when updating the model's language weights
language_update_speed = 0.15

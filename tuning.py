# === Model settings

# Range of years model should simulate
model_years_range = (1965, 1990)

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
reference_chance = 0.96

# Degree to which reference count affects attractability of article on references
reference_count_attractability = 0.3

# Factor applied to article attractiveness by each year that passes by
reference_age_unattractiveness = 0.1

# The starting level of access authors will have over articles in languages they don't know
starting_access_level = 0.02

# How much the access level raises each year
yearly_access_level_increment = 0.02

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
initial_author_count = 2000

# Range of new authors per month
new_author_range = (2, 20)

# How much the new authors count gets skewed to the centers
new_author_skew = 1

# Range of articles published per author
author_lifespan_range = (1, 20)

# How much the author's lifespan gets skewed to the center
author_lifespan_skew = 2

# Chance of generating an extra language in each iteration
chance_of_extra_language = 0.35

# How much authors competencies tend to be pushed to 0.5
author_competency_skew = 4

import csv
from pprint import pprint
from src.author import Author
from src.model import ArticlesModel
from tuning import initial_author_count, model_years_range
from utils.months import Month

# Create model
model = ArticlesModel(initial_author_count)

# model.step(1965, 6)
# exit()

# For each year
for year_index in range(model_years_range[1] - model_years_range[0]):

    # Get current year
    current_year = model_years_range[0] + year_index

    print(
        f"Year {current_year}: {len(model.published_articles)} articles, {model.author_count} authors ({model.active_author_count} active)"
    )

    # For each month
    for month_index in range(1, 13):

        # Get current month
        current_month = Month(month_index)

        # Advance the month
        model.step(current_year, current_month)

    # languages
    articles_per_language = {}

    for article in model.published_articles:
        if not articles_per_language.get(article.language):
            articles_per_language[article.language] = 0

        articles_per_language[article.language] += 1

    pprint(
        sorted(articles_per_language.items(), reverse=True, key=lambda item: item[1])[
            :5
        ]
    )


publish_dates = {}

for article in model.published_articles:
    date_key = f"{article.publish_date[0]} of {article.publish_date[1]}"

    if not publish_dates.get(date_key):
        publish_dates[date_key] = 0

    publish_dates[date_key] += 1

pprint(publish_dates)

# languages
articles_per_language = {}

for article in model.published_articles:
    if not articles_per_language.get(article.language):
        articles_per_language[article.language] = 0

    articles_per_language[article.language] += 1

pprint(sorted(articles_per_language.items(), key=lambda item: item[1]))

sorted_articles = sorted(
    model.published_articles,
    reverse=True,
    key=lambda article: len(article.referencing_articles),
)

sorted_articles = [vars(article) for article in sorted_articles]

for article in sorted_articles:
    article["authors"] = [author.name for author in article["authors"]]
    article["references"] = len(article["references"])
    article["referencing_articles"] = len(article["referencing_articles"])
    article["year"] = article["publish_date"][1]
    article["month"] = article["publish_date"][0].name
    del article["publish_date"]
    del article["cost"]
    del article["model"]
    del article["pos"]

# Save the articles
with open("results.csv", "w") as outputFile:
    # These are the column names
    column_names = [
        "name",
        "year",
        "month",
        "referencing_articles",
        "references",
        "unique_id",
        "language",
        "authors",
        "quality",
    ]

    # Start csv writer
    writer = csv.DictWriter(outputFile, fieldnames=column_names)
    writer.writeheader()

    # Write each row
    for article in sorted_articles:
        writer.writerow(article)

top_6 = sorted_articles[:6] + sorted_articles[-6:]

pprint(list(reversed(top_6)))

# pprint(model.yearly_references)

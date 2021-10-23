from pprint import pprint
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

    # For each month
    for month_index in range(1, 13):

        # Get current month
        current_month = Month(month_index)

        # Advance the month
        model.step(current_year, current_month)

publish_dates = {}

for article in model.published_articles:
    date_key = f"{article.publish_date[0]} of {article.publish_date[1]}"

    if not publish_dates.get(date_key):
        publish_dates[date_key] = 0

    publish_dates[date_key] += 1

pprint(publish_dates)

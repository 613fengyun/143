import pandas as pd
import matplotlib.pyplot as plt
import os


# Function to make a pie chart with a legend
def make_pie_chart(sizes, labels, title, filename, explode=None):
    # Set the size of the plot
    plt.figure(figsize=(10, 8))
    # Explode can be set to emphasize a particular part if needed
    if explode:
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
    else:
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

    # Draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()

    # Create a legend outside the pie chart
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # Save the figure
    plt.savefig(filename)
    plt.close()


# Load the CSV file
file_path = r"E:\ECE 143\filtered_reviews(1).csv"
data = pd.read_csv(file_path)

# Confirm that the necessary columns are included in the DataFrame
assert 'Rating' in data.columns, "Column 'Rating' is missing from the DataFrame."
assert 'Source Category' in data.columns, "Column 'Source Category' is missing from the DataFrame."

# Define the image save path
plots_directory = r"E:\ECE 143\pie charts 2"
if not os.path.exists(plots_directory):
    os.makedirs(plots_directory)

# Overall rating distribution pie chart
ratings_counts = data['Rating'].value_counts()
make_pie_chart(sizes=ratings_counts, labels=ratings_counts.index, title='Overall Ratings Distribution',
               filename=os.path.join(plots_directory, 'overall_ratings_distribution_pie.png'))

# Rating distribution of each Source Category pie chart
source_categories = data['Source Category'].unique()
for category in source_categories:
    category_data = data[data['Source Category'] == category]
    rating_counts = category_data['Rating'].value_counts()
    make_pie_chart(sizes=rating_counts, labels=rating_counts.index, title=f'{category} Ratings Distribution',
                   filename=os.path.join(plots_directory, f'{category}_ratings_distribution_pie.png'))

# Unique Products per Source Category pie chart
unique_products_per_category = data.groupby('Source Category')['Product ID'].nunique()
make_pie_chart(sizes=unique_products_per_category, labels=unique_products_per_category.index,
               title='Unique Products per Source Category',
               filename=os.path.join(plots_directory, 'unique_products_per_source_category_pie.png'))

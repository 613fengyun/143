import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load the CSV file
file_path = r"E:\ECE 143\filtered_reviews(1).csv"
data = pd.read_csv(file_path)

# Confirm that the necessary columns are included in the DataFrame
assert 'Rating' in data.columns, "Column 'Rating' is missing from the DataFrame."
assert 'Source Category' in data.columns, "Column 'Source Category' is missing from the DataFrame."

# Define the image save path
plots_directory = r"E:\ECE 143\pie charts"
if not os.path.exists(plots_directory):
    os.makedirs(plots_directory)

# Pie chart for the overall rating distribution
ratings_counts = data['Rating'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(ratings_counts, labels=ratings_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Overall Ratings Distribution')
plt.tight_layout()
plt.savefig(os.path.join(plots_directory, 'overall_ratings_distribution_pie.png'))
plt.close()

# Pie chart for the rating distribution of each Source Category
source_categories = data['Source Category'].unique()
for category in source_categories:
    plt.figure(figsize=(8, 8))
    category_data = data[data['Source Category'] == category]
    rating_counts = category_data['Rating'].value_counts()

    explode = (0.1,) * len(rating_counts)  # Slightly separate each part, can be adjusted as needed
    plt.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=140, explode=explode)
    plt.title(f'{category} Ratings Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_directory, f'{category}_ratings_pie.png'))
    plt.close()

# Pie chart for the number of different Product IDs in each Source Category
unique_products_per_category = data.groupby('Source Category')['Product ID'].nunique()
plt.figure(figsize=(8, 8))
plt.pie(unique_products_per_category, labels=unique_products_per_category.index, autopct='%1.1f%%', startangle=140)
plt.title('Unique Products per Source Category')
plt.tight_layout()
plt.savefig(os.path.join(plots_directory, 'unique_products_per_source_category_pie.png'))
plt.close()

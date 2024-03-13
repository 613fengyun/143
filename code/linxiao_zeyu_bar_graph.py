import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Load the CSV file
file_path = r"E:\ECE 143\filtered_reviews(1).csv"  # Using raw string for Windows file path
data = pd.read_csv(file_path)

# Assert that the necessary columns are present in the DataFrame
assert 'Rating' in data.columns, "Column 'Rating' is missing from the DataFrame."
assert 'Source Category' in data.columns, "Column 'Source Category' is missing from the DataFrame."

# Set the aesthetics for the plots
sns.set(style="whitegrid")
source_categories = data['Source Category'].unique()

# Assert that there are categories present
assert len(source_categories) > 0, "No source categories found in the 'Source Category' column."

# Define the image save path
plots_directory = r"E:\ECE 143\plots"
if not os.path.exists(plots_directory):
    os.makedirs(plots_directory)

# Task 1: Ratings per Category
# Create and save a plot for the overall distribution of ratings across source categories
plt.figure(figsize=(12, 6))
sns.countplot(data=data, x='Rating', hue='Source Category', palette='viridis')
plt.title('Ratings Distribution per Source Category')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.legend(title='Source Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(plots_directory, 'ratings_distribution_per_source_category.png'))
plt.close()

# Create and save a plot for each source category's ratings distribution
for category in source_categories:
    plt.figure(figsize=(12, 6))
    category_data = data[data['Source Category'] == category]

    # Assert that there is data for the current category
    assert not category_data.empty, f"No data found for category '{category}'."

    sns.countplot(data=category_data, x='Rating', hue='Rating', palette='viridis', dodge=False)
    plt.title(f'Ratings Distribution for {category}')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_directory, f'ratings_distribution_{category}.png'))
    plt.close()

# Task 2: Ratings to Price per Category
# Convert product price column to string and extract the lower price bound
data['Price Lower Bound'] = data['Product Price'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)

# Make sure the 'Price Lower Bound' column was created successfully
assert 'Price Lower Bound' in data.columns, "Column 'Price Lower Bound' was not created."

# Create a price category based on the price floor
bins = [0, 10, 20, 30, 40, 50, 100, 200, 500]
labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-100', '100-200', '200-500']
data['Price Category'] = pd.cut(data['Price Lower Bound'], bins=bins, labels=labels, right=False)

# Make sure the 'Price Category' column was successfully created
assert 'Price Category' in data.columns, "Column 'Price Category' was not created."

# Visualize and save the plot of average ratings for different price categories
plt.figure(figsize=(14, 7))
sns.barplot(x='Price Category', y='Rating', hue='Source Category', data=data, palette='coolwarm', ci=None)
plt.title('Average Rating by Price Category per Source Category')
plt.xlabel('Price Category')
plt.ylabel('Average Rating')
plt.legend(title='Source Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(plots_directory, 'average_rating_by_price_category.png'))
plt.close()

# Draw and save a separate chart for each category
for category in data['Source Category'].unique():
    plt.figure(figsize=(14, 7))
    category_data = data[data['Source Category'] == category]

    # Make sure there is data in each category
    assert not category_data.empty, f"No data found for category '{category}'."

    sns.barplot(x='Price Category', y='Rating', data=category_data, palette='coolwarm', ci=None)
    plt.title(f'Average Rating by Price Category for {category}')
    plt.xlabel('Price Category')
    plt.ylabel('Average Rating')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_directory, f'average_rating_by_price_category_for_{category}.png'))
    plt.close()

# Task 3: Items per Category
# Ensure the 'Source Category' and 'Product ID' columns exist
assert 'Source Category' in data.columns, "Column 'Source Category' is missing from the DataFrame."
assert 'Product ID' in data.columns, "Column 'Product ID' is missing from the DataFrame."

# Group by 'Source Category' and count unique 'Product ID's
unique_products_per_category = data.groupby('Source Category')['Product ID'].nunique().reset_index()

# Verify that the operation was successful
assert 'Product ID' in unique_products_per_category.columns, "Column 'Product ID' is missing after grouping."

# Create, visualize, and save the number of unique products per source category
plt.figure(figsize=(12, 6))
barplot = sns.barplot(x='Source Category', y='Product ID', data=unique_products_per_category, palette='muted')
plt.title('Number of Unique Products per Source Category')
plt.xlabel('Source Category')
plt.ylabel('Number of Unique Products')
plt.xticks(rotation=45)
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.0f'),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center',
                     xytext=(0, 9),
                     textcoords='offset points')
plt.tight_layout()
plt.savefig(os.path.join(plots_directory, 'unique_products_per_source_category.png'))
plt.close()


# Function to handle price conversion
def handle_price(price_str):
    # Remove the dollar sign and spaces, and replace the range separator with a standard '-'
    price_str = price_str.replace('$', '').replace(' ', '').replace('–', '-')

    # Split the price range and calculate the average
    if '-' in price_str:
        parts = price_str.split('-')
        try:
            # Attempt to convert to float and calculate the average
            numbers = list(map(float, parts))
            return sum(numbers) / len(numbers)
        except ValueError:
            # If conversion fails, return NaN
            return pd.NA
    else:
        try:
            # Attempt to convert a single price to float
            return float(price_str)
        except ValueError:
            # If conversion fails, return NaN
            return pd.NA


data['Price'] = data['Product Price'].astype(str).apply(handle_price)

# Plotting Average and Median Prices by Rating for each category
for category in source_categories:
    category_data = data[data['Source Category'] == category]
    if not category_data.empty:
        # Group data by 'Rating' and aggregate 'Price' with 'mean' and 'median'
        price_stats = category_data.groupby('Rating')['Price'].agg(['mean', 'median']).reset_index()
        melted_price_stats = price_stats.melt(id_vars='Rating', value_vars=['mean', 'median'],
                                              var_name='Price Type', value_name='Price')

        # Plotting
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Rating', y='Price', hue='Price Type', data=melted_price_stats, palette=['skyblue', 'coral'])
        plt.title(f'Average and Median Prices by Rating for {category}')
        plt.xlabel('Rating')
        plt.ylabel('Price ($)')
        plt.tight_layout()
        # Saving the plot
        plt.savefig(os.path.join(plots_directory, f'avg_median_prices_{category}.png'))
        plt.close()

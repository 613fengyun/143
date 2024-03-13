import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def load_data(filename):
    """
    Load the CSV file and return the DataFrame.

    Parameters:
    filename (str): The file path of the CSV file.

    Returns:
    pandas.DataFrame: The loaded data.
    """
    return pd.read_csv(filename)


def assert_columns(data, columns):
    """
    Assert that the necessary columns are present in the DataFrame.

    Parameters:
    data (pandas.DataFrame): The DataFrame to check.
    columns (list of str): The list of column names to check for in the DataFrame.
    """
    for column in columns:
        assert column in data.columns, f"Column '{column}' is missing from the DataFrame."



def create_plots_directory(plots_directory):
    """
    Create the directory if it does not exist.

    Parameters:
    plots_directory (str): The path of the directory where the plots will be saved.
    """
    if not os.path.exists(plots_directory):
        os.makedirs(plots_directory)



def plot_category_ratings_distribution(data, plots_directory, source_categories):
    """
    Create and save plots for each source category's ratings distribution.

    Parameters:
    data (pandas.DataFrame): The data containing the ratings and source categories.
    plots_directory (str): The directory where the plots will be saved.
    source_categories (list): A list of unique source categories.
    """
    for category in source_categories:
        plt.figure(figsize=(12, 6))
        category_data = data[data['Source Category'] == category]

        sns.countplot(data=category_data, x='Rating', hue='Rating', palette='viridis', dodge=False)
        plt.title(f'Ratings Distribution for {category}')
        plt.xlabel('Rating')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(plots_directory, f'ratings_distribution_{category}.png'))
        plt.close()
def plot_average_rating_by_price_category(data, plots_directory):
    """
    Create and save a plot for the average ratings for different price categories.

    Parameters:
    data (pandas.DataFrame): The data containing the ratings and product prices.
    plots_directory (str): The directory where the plots will be saved.
    """
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Price Category', y='Rating', hue='Source Category', data=data, palette='coolwarm', ci=None)
    plt.title('Average Rating by Price Category per Source Category')
    plt.xlabel('Price Category')
    plt.ylabel('Average Rating')
    plt.legend(title='Source Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_directory, 'average_rating_by_price_category.png'))
    plt.close()
def plot_unique_products_per_source_category(data, plots_directory):
    """
    Create and save a plot for the number of unique products per source category.

    Parameters:
    data (pandas.DataFrame): The data containing the source categories and product IDs.
    plots_directory (str): The directory where the plots will be saved.
    """
    unique_products_per_category = data.groupby('Source Category')['Product ID'].nunique().reset_index()

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


def handle_price(price):
    """
    Convert a price string to a float. If it's a range, return the average.

    Parameters:
    price (str or float): The price value to convert.

    Returns:
    float or pd.NA: The converted price as a float, or pd.NA if conversion fails.
    """
    # If the price is already a float (non-string), then we don't need to do any processing
    if isinstance(price, float) and not np.isnan(price):
        return price

    try:
        # If price is not a float or it's NaN, assume it's a string and clean it
        price_str = str(price)
        price_str = price_str.replace('$', '').replace(' ', '').replace('–', '-')

        if '-' in price_str:
            parts = price_str.split('-')
            numbers = list(map(float, parts))
            return sum(numbers) / len(numbers)
        else:
            return float(price_str)
    except (ValueError, TypeError):
        return pd.NA


def plot_avg_and_median_prices_by_rating_for_category(category_data, plots_directory, category_name):
    """
    Create and save a plot showing the average and median prices by rating for a given category.

    Parameters:
    category_data (pandas.DataFrame): The data for the specific category.
    plots_directory (str): The directory where the plot will be saved.
    category_name (str): The name of the category being processed.
    """
    # First, calculate the average and median prices for each rating level
    price_stats = category_data.groupby('Rating')['Price Lower Bound'].agg(['mean', 'median']).reset_index()

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Plot the average price
    sns.lineplot(x='Rating', y='mean', data=price_stats, marker='o', label='Average Price', color='blue')

    # Plot the median price
    sns.lineplot(x='Rating', y='median', data=price_stats, marker='o', label='Median Price', color='red')

    # Add chart title and axis labels
    plt.title(f'Average and Median Prices by Rating for {category_name}')
    plt.xlabel('Rating')
    plt.ylabel('Price')

    # Add legend
    plt.legend()

    # Tight layout
    plt.tight_layout()

    # Save the chart
    plt.savefig(os.path.join(plots_directory, f'avg_median_prices_{category_name}.png'))

    # Close the plot to start drawing the next one
    plt.close()

def plot_overall_rating_distribution(data, plots_directory):
    """
    Create and save a pie chart for the overall rating distribution.

    Parameters:
    data (pandas.DataFrame): The dataset.
    plots_directory (str): The directory where the plot will be saved.
    """
    ratings_counts = data['Rating'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(ratings_counts, labels=ratings_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Overall Ratings Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_directory, 'overall_ratings_distribution_pie.png'))
    plt.close()


def plot_rating_distribution_per_source_category(data, plots_directory):
    """
    Create and save a pie chart for the rating distribution of each Source Category.

    Parameters:
    data (pandas.DataFrame): The dataset.
    plots_directory (str): The directory where the plots will be saved.
    """
    source_categories = data['Source Category'].unique()
    for category in source_categories:
        plt.figure(figsize=(8, 8))
        category_data = data[data['Source Category'] == category]
        rating_counts = category_data['Rating'].value_counts()

        explode = (0.1,) * len(rating_counts)  # Slightly separate each part
        plt.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=140, explode=explode)
        plt.title(f'{category} Ratings Distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(plots_directory, f'{category}_ratings_pie.png'))
        plt.close()


def plot_unique_products_per_source_category(data, plots_directory):
    """
    Create and save a pie chart for the number of different Product IDs in each Source Category.

    Parameters:
    data (pandas.DataFrame): The dataset.
    plots_directory (str): The directory where the plot will be saved.
    """
    unique_products_per_category = data.groupby('Source Category')['Product ID'].nunique()
    plt.figure(figsize=(8, 8))
    plt.pie(unique_products_per_category, labels=unique_products_per_category.index, autopct='%1.1f%%', startangle=140)
    plt.title('Unique Products per Source Category')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_directory, 'unique_products_per_source_category_pie.png'))
    plt.close()


def main():
    # File path and plots saving path
    file_path = r"E:\ECE 143\filtered_reviews(1).csv"
    plots_directory = r"E:\ECE 143\plots"

    # Load data and assert necessary columns
    data = pd.read_csv(file_path)
    assert 'Rating' in data.columns, "Column 'Rating' is missing from the DataFrame."
    assert 'Source Category' in data.columns, "Column 'Source Category' is missing from the DataFrame."

    # Set chart aesthetics
    sns.set(style="whitegrid")

    # Create directory for saving charts
    if not os.path.exists(plots_directory):
        os.makedirs(plots_directory)

    # Process prices and create price categories
    data['Price'] = data['Product Price'].astype(str).apply(handle_price)
    data['Price Lower Bound'] = data['Price'].fillna(0)
    bins = [0, 10, 20, 30, 40, 50, 100, 200, 500]
    labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-100', '100-200', '200-500']
    data['Price Category'] = pd.cut(data['Price Lower Bound'], bins=bins, labels=labels, right=False)

    # Perform visualization tasks
    source_categories = data['Source Category'].unique()
    plot_category_ratings_distribution(data, plots_directory, source_categories)
    plot_average_rating_by_price_category(data, plots_directory)
    plot_unique_products_per_source_category(data, plots_directory)
    plot_overall_rating_distribution(data, plots_directory)
    plot_rating_distribution_per_source_category(data, plots_directory)
    plot_unique_products_per_source_category(data, plots_directory)

    # Plot charts for average and median prices by rating for each category
    for category in source_categories:
        category_data = data[data['Source Category'] == category]
        if not category_data.empty:
            plot_avg_and_median_prices_by_rating_for_category(category_data, plots_directory, category)

if __name__ == "__main__":
    main()






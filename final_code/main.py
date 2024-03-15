'''
Main script that contains all of the parsing and graph creation. 
'''
import pandas as pd #3rd-party
import matplotlib.pyplot as plt #3rd-party
import seaborn as sns #3rd-party
import numpy as np #3rd-party
import os
import csv
import json
from collections import Counter
from wordcloud import WordCloud
import string
from nltk.corpus import stopwords  # Assuming NLTK is installed #3rd-party
import nltk #3rd-party

# File path and plots saving path
INPUT_CSV = "truncated_filtered_reviews.csv"
plots_directory = "temp_plots/"

'''
CONNOR'S TASKS
==============================
'''
def verified_review_ratings(filename):
    '''
    Finds the Ratings and verified reviews
    input - parsed csv file with review data
    '''
    assert(isinstance(filename,str))
    with open(filename, 'r', encoding='UTF8') as f:
        reader = csv.DictReader(f)
        outputDict = {"verified-ratings": {"1.0": 0,
                                   "2.0": 0,
                                   "3.0": 0,
                                   "4.0": 0,
                                   "5.0": 0},
                      "unverified-ratings": {"1.0": 0,
                                   "2.0": 0,
                                   "3.0": 0,
                                   "4.0": 0,
                                   "5.0": 0}}
        for line in reader:
            verified = line["Verified"]
            if verified.lower() == "true":
                verified = True
            else: verified = False
            if verified:
                outputDict["verified-ratings"][str(line["Rating"])] += 1
            else:
                outputDict["unverified-ratings"][str(line["Rating"])] += 1
    return outputDict

# Could combine the two for faster run time but keeping separate to make it clear between the prompts

#DOCSTRING
def word_freq(filename):
    '''
    Finds the counts of each word in the review text
    input - the parsed csv file
    '''
    assert(isinstance(filename, str))
    with open(filename, 'r', encoding="UTF8") as f:
        symbols = "!@#$%^&*()_+-=[]\\{}|,./<>?:\";\'"
        reader = csv.DictReader(f)
        outputDict = {}
        stopwords = set(nltk.corpus.stopwords.words('english'))
        for line in reader:
            words = line["Review Text"].split()
            for word in words:
                word = word.lower()
                for char in symbols:
                    #remove symbols to just filter out people that don't use symbols and punctuation
                    word = word.replace(char, "")
                if word in stopwords or word == '':
                    continue
                try:
                    outputDict[word] += 1
                except KeyError:
                    outputDict[word] = 1
    counts = Counter(outputDict).most_common(100)
    outputDict = {}
    for count in counts:
        outputDict[count[0]] = count[1]
    return outputDict

def make_wordcloud(input_dict):
    assert(isinstance(input_dict, dict))
    wc = WordCloud(background_color="white", max_words=1000)
    wc.generate_from_frequencies(input_dict)

    # display graph
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.savefig(os.path.join(plots_directory, 'all_cats_wordcloud.png'))
    plt.show()
    #plt.close()

#Reference Source https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
def make_verfied_charts(input_dict):
    X = ["1.0", "2.0", "3.0", "4.0", "5.0"]
    X2 = ["Verified", "Unverified"]
    YVerified = []
    YUnverified = []
    YCounts = [0, 0]
    for key in input_dict["verified-ratings"]:
        YVerified.append(input_dict["verified-ratings"][key])
        YCounts[0] += input_dict["verified-ratings"][key]

    for key in input_dict["unverified-ratings"]:
        YUnverified.append(input_dict["unverified-ratings"][key])
        YCounts[1] += input_dict["unverified-ratings"][key]

    fig, (ax3) = plt.subplots(1,1)
    ax3.pie(YCounts, labels=X2, autopct='%1.1f%%')
    fig.suptitle("Proportion of Verified Reviews")
    #plt.savefig(os.path.join(plots_directory, 'verified_proportions.png'))
    plt.show()
    #plt.close()

    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.suptitle("Counts by Verified Status")
    ax1.pie(YVerified, labels=X, autopct='%1.1f%%')
    ax1.set_title("Verified Reviews")
    ax2.pie(YUnverified, labels=X, autopct='%1.1f%%')
    ax2.set_title("Unverified Reviews")
    #plt.savefig(os.path.join(plots_directory, 'verified_ratings.png'))
    plt.show()
    #plt.close()

'''
ZEYU'S & LINXIAO'S TASKS
==============================
'''

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
    #plt.savefig(os.path.join(plots_directory, 'average_rating_by_price_category.png'))
    plt.show()
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

    price_stats.set_index("Rating").plot.bar()
    # Add chart title and axis labels
    plt.title(f'Average and Median Prices by Rating for {category_name}')
    plt.xlabel('Rating')
    plt.ylabel('Price')

    # Add legend
    plt.legend()

    # Save the chart
    #plt.savefig(os.path.join(plots_directory, f'avg_median_prices_{category_name}.png'))

    # Close the plot to start drawing the next one
    plt.show()
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
    #plt.savefig(os.path.join(plots_directory, 'overall_ratings_distribution_pie.png'))
    plt.show()
    plt.close()

'''
SAHIL'S TASKS
==============================
'''
def preprocess_text(text):
  """
  Preprocesses text for better word analysis.

  Args:
      text: A string containing text to be preprocessed.

  Returns:
      A string containing the preprocessed text.
  """
  if len(text)>10000000:
      text = text[:10000000]
  # Lowercase all characters
  text = text.lower()

  # Remove punctuation (consider using a regular expression for more flexibility)
  punc = set(string.punctuation)
  text = "".join([char for char in text if char not in punc])

  # Remove stopwords (using NLTK)
  stop_words = set(stopwords.words('english'))
  text = " ".join([word for word in text.split() if word not in stop_words])

  # Additional preprocessing steps (optional):
  # - Stemming or lemmatization (reduce words to their base forms)
  # - Remove special characters or HTML tags

  return text

def visualize_top_words(df, n_words=5):
    """
    Creates bar charts and word counts showing the top n most common words for each category and also per rating.

    Args:
        df: A pandas DataFrame containing columns like 'category' and 'review_text'.
        n_words: The number of most common words to display (default: 5).
    """
    filename = INPUT_CSV
    df = pd.read_csv(filename, encoding='utf-8')
    df['Review Text'] = df['Review Text'].astype(str)
    categories = df['Source Category'].unique()

    ratings = list(range(1,6))
    for category in categories:
        print(f'Starting with {category} category')
        filtered_by_category = df[df['Source Category'] == category]
        if not len(filtered_by_category):
                continue
        # Combine all review text for this category into a single string
        all_text = " ".join(filtered_by_category['Review Text'])

        # Preprocess text (optional): lowercase, remove stopwords, punctuation
        # (consider using NLTK for advanced text processing)
        all_text = preprocess_text(all_text)

        # Create a WordCloud object
        #wordcloud = WordCloud(width=800, height=600).generate(all_text)

        # Create a Counter object to count word frequencies
        word_counts = Counter(all_text.split())

        # Get the top n most common words
        top_n_words = word_counts.most_common(n_words)

        # Extract words and counts for the bar chart
        words, counts = zip(*top_n_words)

        # Create a new figure for the wordcloud
        #plt.figure()
        #plt.imshow(wordcloud, interpolation='bilinear')
        #plt.axis('off')
        #plt.title(f"Most Common Words in Reviews (Category: {category})")
        #plt.show()
        #plt.savefig(f"{category[:-5]}")
        #plt.close()

        # Create a new figure for the bar chart
        plt.figure()
        plt.bar(words, counts)
        plt.xlabel("Word")
        plt.ylabel("Frequency")
        plt.title(f"Top {n_words} Words in Reviews (Category: {category})")
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.show()
        #plt.savefig(f"{category[:-5]} bar chart")
        plt.close()
        ''' REMOVING THE RATINGS SINCE NOT USED IN THE PRESENTATION
        for rating in ratings:
            print(f'Starting with {rating} rating products for {category} category')
            filtered_df = filtered_by_category[filtered_by_category['Rating'] == rating]
            if not len(filtered_df):
                continue
            # Combine all review text for this category into a single string
            all_text = " ".join(filtered_df['Review Text'])

            # Preprocess text (optional): lowercase, remove stopwords, punctuation
            # (consider using NLTK for advanced text processing)
            all_text = preprocess_text(all_text)

            # Create a WordCloud object
            wordcloud = WordCloud(width=800, height=600).generate(all_text)

            # Create a Counter object to count word frequencies
            word_counts = Counter(all_text.split())

            # Get the top n most common words
            top_n_words = word_counts.most_common(n_words)

            # Extract words and counts for the bar chart
            words, counts = zip(*top_n_words)

            # Create a new figure for the wordcloud
            plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f"Most Common Words in Reviews (Category: {category})")
            plt.show()
            #plt.savefig(f"{category[:-5]} {rating}")
            plt.close()

            # Create a new figure for the bar chart
            plt.figure()
            plt.bar(words, counts)
            plt.xlabel("Word")
            plt.ylabel("Frequency")
            plt.title(f"Top {n_words} Words in Reviews (Category: {category})")
            plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
            plt.tight_layout()
            plt.show()
            #plt.savefig(f"{category[:-5]} {rating} bar chart")
            plt.close()'''

def count_word_occurrences(text, word):
  """
  Counts the frequency of the word "good" and the phrase "not good" in a string.

  Args:
      text: The string to analyze.

  Returns:
      A dictionary containing counts for "good", "not good", and the total number of words.
  """
  if len(text)>10000000:
      text = text[:10000000]
  word_counts = {"good": 0, "not good": 0, "total_words": 0}
  text = text.lower()  # Convert to lowercase for case-insensitive counting

  # Split the text into words
  words = text.split()
  word_counts["total_words"] = len(words)

  # Count occurrences of "good" and "not good"
  for i in range(len(words)):
    if (words[i] == "not" and i + 1 < len(words) and words[i + 1] == word): #or words[i] == "bad":  # Check for "not good" phrase
      word_counts["not good"] += 1
    elif words[i] == word:
      word_counts["good"] += 1

  return word_counts

def visualize_word_usage_over_ratings(df, word):
    """
    Counts
    """
    filename = INPUT_CSV
    df = pd.read_csv(filename, encoding='utf-8')
    df['Review Text'] = df['Review Text'].astype(str)
    categories = df['Source Category'].unique()

    ratings = list(range(1,6))
    for category in categories:
        good_count = {}
        not_good_count = {}
        if word == "comfortable" and "AMAZON_FASHION" not in category:
            continue
        #print(f'Starting with {category} category')
        filtered_by_category = df[df['Source Category'] == category]
        if not len(filtered_by_category):
                continue
        for rating in ratings:
            #print(f'Starting with {rating} rating products for {category} category')
            filtered_df = filtered_by_category[filtered_by_category['Rating'] == rating]
            if not len(filtered_df):
                continue
            # Combine all review text for this category into a single string
            all_text = " ".join(filtered_df['Review Text'])
            count = count_word_occurrences(all_text, word)
            good_count[rating] = count['good']
            not_good_count[rating] = count['not good']
        
        good_count = sorted((float(x),y) for x, y in good_count.items())
        x_vals = [x for x, _ in good_count]
        y_vals = [y for _, y in good_count]

        # Create the line graph
        plt.plot(x_vals, y_vals, color='blue', linestyle='-')
        # plt.plot(list(not_good_count.keys()), list(not_good_count.values()), color='red', linestyle='-')

        # Add labels and title
        plt.xlabel('Ratings')
        plt.ylabel('Frequency of occurence of the words')
        plt.title(f'Line Graph For Usage of {word} in {category[:-5]}')

        # Add grid lines
        plt.grid(True)

        plt.show()
        #plt.savefig(f"{category[:-5]} line chart")
        plt.close()

'''
MAIN FUNCTIONS
'''

def zeyu_linxiao_main():
    # ZEYU LINXIAO PROCESSING
    # Load data and assert necessary columns
    data = pd.read_csv(INPUT_CSV)
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
    plot_average_rating_by_price_category(data, plots_directory)
    plot_overall_rating_distribution(data, plots_directory)

    # Plot charts for average and median prices by rating for each category
    for category in source_categories:
        if category not in ["Office_Products_5.json","Toys_and_Games_5.json"]:continue
        category_data = data[data['Source Category'] == category]
        if not category_data.empty:
            plot_avg_and_median_prices_by_rating_for_category(category_data, plots_directory, category)

def connor_main():
    output = verified_review_ratings(INPUT_CSV)
    nltk.download('stopwords')
    output["Word Frequencies"] = word_freq(INPUT_CSV)
    make_verfied_charts(output)
    make_wordcloud(output["Word Frequencies"])

def sahil_main():
    filename = INPUT_CSV
    df = pd.read_csv(filename, encoding='utf-8')
    df['Review Text'] = df['Review Text'].astype(str)
    word = 'good'
    visualize_top_words(df.copy())
    visualize_word_usage_over_ratings(df, word)
    word = 'comfortable'
    visualize_word_usage_over_ratings(df, word)

#connor_main()
#zeyu_linxiao_main()
#sahil_main()
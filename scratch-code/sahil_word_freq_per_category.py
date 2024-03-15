import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from nltk.corpus import stopwords  # Assuming NLTK is installed

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
        # plt.show()
        plt.savefig(f"{category[:-5]}")
        plt.close()

        # Create a new figure for the bar chart
        plt.figure()
        plt.bar(words, counts)
        plt.xlabel("Word")
        plt.ylabel("Frequency")
        plt.title(f"Top {n_words} Words in Reviews (Category: {category})")
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
        plt.tight_layout()
        # plt.show()
        plt.savefig(f"{category[:-5]} bar chart")
        plt.close()
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
            # plt.show()
            plt.savefig(f"{category[:-5]} {rating}")
            plt.close()

            # Create a new figure for the bar chart
            plt.figure()
            plt.bar(words, counts)
            plt.xlabel("Word")
            plt.ylabel("Frequency")
            plt.title(f"Top {n_words} Words in Reviews (Category: {category})")
            plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
            plt.tight_layout()
            # plt.show()
            plt.savefig(f"{category[:-5]} {rating} bar chart")
            plt.close()

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
    ratings = list(range(1,6))
    good_count = {}
    not_good_count = {}
    for category in categories:
        print(f'Starting with {category} category')
        filtered_by_category = df[df['Source Category'] == category]
        if not len(filtered_by_category):
                continue
        for rating in ratings:
            print(f'Starting with {rating} rating products for {category} category')
            filtered_df = filtered_by_category[filtered_by_category['Rating'] == rating]
            if not len(filtered_df):
                continue
            # Combine all review text for this category into a single string
            all_text = " ".join(filtered_df['Review Text'])
            count = count_word_occurrences(all_text, word)
            good_count[rating] = count['good']
            not_good_count[rating] = count['not good']
        # Create the line graph
        plt.plot(list(good_count.keys()), list(good_count.values()), color='blue', linestyle='-')
        # plt.plot(list(not_good_count.keys()), list(not_good_count.values()), color='red', linestyle='-')

        # Add labels and title
        plt.xlabel('Ratings')
        plt.ylabel('Frequency of occurence of the words')
        plt.title(f'Line Graph For Usage of Words in {category[:-5]}')

        # Add grid lines
        plt.grid(True)

        plt.savefig(f"{category[:-5]} line chart")
        plt.close()




if __name__=="__main__":
    # filename = 'shuffled_data.csv'
    filename = '/Users/sahilmehra/Downloads/filtered_reviews.csv'
    df = pd.read_csv(filename, encoding='utf-8')
    df['Review Text'] = df['Review Text'].astype(str)
    categories = df['Source Category'].unique()
    word = 'comfortable'

    visualize_top_words(df.copy())
    visualize_word_usage_over_ratings(df, word)

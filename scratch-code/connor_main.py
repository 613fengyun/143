import csv
import json
import nltk
from collections import Counter
from wordcloud import WordCloud

def verified_review_ratings(filename):
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

#output = verified_review_ratings("filtered_reviews.csv")
#print(output)
#nltk.download('stopwords')
#output["Word Frequencies"] = word_freq("filtered_reviews.csv")
#print(output)
#with open("datafile.json", 'w', encoding="UTF8") as f:
#    f.write(json.dumps(output, indent=4))

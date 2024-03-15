from wordcloud import WordCloud
import json
import matplotlib.pyplot as plt
import numpy as np



def make_wordcloud(input_dict):
    wc = WordCloud(background_color="white", max_words=1000)
    wc.generate_from_frequencies(input_dict)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

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

    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.suptitle("Counts by Verified Status")
    ax1.pie(YVerified, labels=X, autopct='%1.1f%%')
    ax1.set_title("Verified Reviews")
    ax2.pie(YUnverified, labels=X, autopct='%1.1f%%')
    ax2.set_title("Unverified Reviews")
    plt.show() 

    fig, (ax3) = plt.subplots(1,1)
    ax3.pie(YCounts, labels=X2, autopct='%1.1f%%')
    fig.suptitle("Proportion of Verified Reviews")
    plt.show()

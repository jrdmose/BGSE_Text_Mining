import matplotlib.pyplot as plt
from wordcloud import WordCloud
from types import *

def plot_wordcloud(tweets, save_path = None):

    # Transform input in a list of words
    words = []
    if isinstance(tweets[0], list):
        for tweet in tweets:
            words += tweet

    if isinstance(tweets[0], str):
        words = tweets

    # Compute word frequency
    freq = {}
    for word in words:
        if freq.get(word):
            freq[word] +=1
        else:
            freq[word] = 1



    wordcloud = WordCloud(width = 800, height = 600,
                    background_color ='white',
                    max_words = 100,
                    min_font_size = 10,
                    regexp = r"\w+").generate_from_frequencies(freq)

    # plot the WordCloud image
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    if save_path:
        wordcloud.to_file(save_path)

    plt.imshow(wordcloud)
    plt.show()

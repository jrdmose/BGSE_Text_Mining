import matplotlib.pyplot as plt
from wordcloud import WordCloud

def plot_wordcloud(words):

    words = ' '.join([' '.join(tweet) for tweet in words])

    wordcloud = WordCloud(width = 800, height = 600,
                    background_color ='white',
                    max_words = 100,
                    min_font_size = 10).generate(words)

    # plot the WordCloud image
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()

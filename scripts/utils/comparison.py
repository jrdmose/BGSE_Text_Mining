from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD, PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function for showing most similar words by model
def get_most_similar(models,word,n_similar, model_names):

    # First
    colnames = [model_names[0] + x for x in [" - Word"," - Similarity"]]

    df = pd.DataFrame(models[0].wv.most_similar(positive = [word],topn=n_similar), columns = colnames)

    if len(models) > 1:
        for i,model in enumerate(models[1:]):

            colnames = [model_names[i+1] + x for x in [" - Word"," - Similarity"]]

            df = pd.concat((df,pd.DataFrame(models[i+1].wv.most_similar(positive = [word]), columns = colnames)), axis=1)
    print(f"Most similar words per model for word: {word}")
    return df

# Function for running pca and t-sne on word vectors to plot afterwords
def embedd_tSNE(data_array,pca_n = 10, metric ='cosine'):

    print("starting PCA")

    # Use PCA  to cut down dimensionality of input array
    # We use PCA because we have a dense matrix (used TruncSVD in Nandan exercise because of count Vectorizer = sparse)
    data_reduced = PCA(n_components=pca_n).fit_transform(data_array)

    print("Done with PCA")

    # Use t-SNE on pca data
    d = TSNE(metric=metric, n_components=2,perplexity=15).fit_transform(data_reduced)

    return d


# Function for getting two words and similar words as vectors to compare them later
def compare_words(w1, w2, n_comparison, w2v_model):

    # Store in list
    word_list = [w1,w2]

    # Colors for plotting
    word_colr = ["orange","lightblue"]

    # Get lists of n most similar words
    close_w1 = w2v_model.wv.most_similar([w1],topn=n_comparison)
    close_w2 = w2v_model.wv.most_similar([w2],topn=n_comparison)

    # Store these words as well in the word_list
    close1_words = [w[0] for w in close_w1]
    close2_words = [w[0] for w in close_w2]

    # Append to word list
    word_list = np.append(word_list, [close1_words, close2_words])

    # Append word_colr
    word_colr = np.append(word_colr, [np.repeat("red",n_comparison), np.repeat("blue",n_comparison)])

    ## Set up empty array to store vectors in
    # Get dimensionality of the array based on dim of embeddings
    arrays_dim = w2v_model.wv.__getitem__([w1]).shape[1]

    # Set up empty array to fill later
    word_array = np.empty((0, arrays_dim), dtype = 'f')

    # Go through each word, store its vector in array
    for word in word_list:

        # Get vector
        wrd_vec= w2v_model.wv.__getitem__([word])

        # Append to array
        word_array = np.append(word_array, wrd_vec, axis=0)

    return word_list, word_colr, word_array

# Function for plotting the word embeddings
def plot_word_embeddings(w1,w2, n_comparison, w2v_model):

    # Get arrays, word_list and groups
    word_list, word_colr, word_array = compare_words(w1,w2, n_comparison,w2v_model)

    # Embedd them using PCA and t-SNE
    embedded  = embedd_tSNE(word_array,pca_n = n_comparison, metric ='cosine')

    # Store results in data frame
    plot_df = pd.DataFrame({'x': [x for x in embedded[:, 0]],
                            'y': [y for y in embedded[:, 1]],
                            'words': word_list,
                            'color': word_colr})

    # Set up figure
    fig, _ = plt.subplots(figsize = (12,8))

    # Pot using regplot
    p= sns.regplot(data=plot_df,
                         x="x",
                         y="y",
                         fit_reg=False,
                         marker="o",
                         scatter_kws={'s': 40,
                                      'facecolors':plot_df['color']})

    # Annotate
    for line in range(0, plot_df.shape[0]):
             p.text(plot_df["x"][line],
                     plot_df['y'][line],
                     '  ' + plot_df["words"][line].title(),
                     horizontalalignment='left',
                     verticalalignment='bottom', size='medium',
                     color=plot_df['color'][line],
                     weight='normal'
                    ).set_size(15)

    plt.xlim(plot_df.x.min()-50, plot_df.x.max()+50)
    plt.ylim(plot_df.y.min()-50, plot_df.y.max()+50)

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pickle
import re

# open the lyrics
path = 'documents.pickle'
with open(path, 'rb') as handle:
    documents = pickle.load(handle)

# remove the stop words
stopwords = set(STOPWORDS)

# print a word cloud for each artist
for artist in documents:

    text = ''.join(documents[artist]['document'])
    text = text.lower()
    text=text.strip()
    text=re.sub("\n","",text)
    text=re.sub("'","",text)

    wordcloud = WordCloud(background_color="white",
                          width = 800,
                          height = 800,
                          stopwords = stopwords,
                          min_font_size = 10).generate(text)
    
    # plt.figure(figsize=(20,15))
    
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(artist + '.png', dpi=100)
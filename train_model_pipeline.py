from sklearn.pipeline import make_pipeline
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
import re
from sklearn.preprocessing import FunctionTransformer
from functions import re_transform, list_re_transform, make_corpus_labels

# open the lyrics from the pickle file
with open('documents.pickle', 'rb') as handle:
    documents = pickle.load(handle)

# create corpus and labels
corpus, labels = make_corpus_labels(documents)

# split data 
Xtrain, Xtest, ytrain, ytest = train_test_split(corpus, labels, random_state=40)

# create the pipelines
# !TODO this model can probably be improved with a parameter grid search  
pipeline = make_pipeline(FunctionTransformer(list_re_transform),
                         TfidfVectorizer(stop_words='english',
                                         ngram_range=(1, 1)), 
                         RandomForestClassifier(max_depth=2))

# fit the model
pipeline.fit(Xtrain, ytrain)

# print train and test score
print(f'train: {pipeline.score(Xtrain, ytrain)}')
print(f'test: {pipeline.score(Xtest, ytest)}')

# type in your own lyrics to test the model 
print(pipeline.predict_proba(['hey you! what ya doing over there? i can see whats on your mind']))
print(pipeline.classes_)
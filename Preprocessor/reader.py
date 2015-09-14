from bs4 import BeautifulSoup
import glob
import string
import math
import csv
from collections import Counter
from nltk.corpus import stopwords

allfiles = glob.glob("../DataSet/*000.sgm")
tags = ['topics', 'places', 'title', 'dateline', 'body']
stop = stopwords.words('english')

# To count the total number of articles
articles = 0

# Dictionary storing all the documents and word frequencies
tf = {}

# List to store unique words per article to find in how many articles a word is appearing
uniqueWords = []

# Reading file and creating Term Frequencies per article
for datafile in allfiles:
    f = open(datafile, 'r')
    soup = BeautifulSoup(f.read(), "html.parser")

    for article in soup.findAll('reuters'):
        words = []
        articles += 1
        for tag in tags:
            text = article.find(tag)
            if text:
                text = text.text.encode("ascii", "ignore")
                final_string = text.translate(None, string.punctuation).lower()
                filtered_words = [word for word in final_string.split() if word not in stop]
                words += filtered_words
        tf[articles] = Counter(words)
        uniqueWords += tf[articles].keys()

    print datafile + " done"

# Count of how many articles a word is appearing in
appearance = Counter(uniqueWords)

# Saving inverse document frequencies
idf = {}

# Counting the IDF for all the words
for word in appearance.keys():
    idf[word] = math.log10(articles / appearance[word])

# Saving TF-IDF values for all the words per article
tf_Idf = tf.copy()

# Storing most common 1000 words per article
allWords = []

# Counting the TF-IDF for each word and storing most common 500 words in allWords
for i in tf_Idf.keys():
    art = tf_Idf[i]
    for word in art.keys():
        art[word] *= idf[word]
    allWords += art.most_common(1000)

# Sorting all the words according to TF-IDF value
allWords.sort(key=lambda tup: tup[1], reverse=True)

# Filtering out unique words
seen = set()

# List containing words with highest TF-IDF
feature_words = []

# Filtering unique words
for word, val in allWords:
    if word not in seen:
        feature_words.append(word)
        seen.add(word)

# Filtering top 1000 words
feature_words = feature_words[:1000]

# For storing the feature vector
feature_vector = []

# First column of the matrix representing document-id
heading = ['documentId']
heading.extend(feature_words)

feature_vector.append(heading)

for i in tf_Idf.keys():
    row = [i]
    for word in feature_words:
        if word in tf_Idf[i]:
            row.append(tf_Idf[i][word])
        else:
            row.append(0)
    feature_vector.append(row)

with open('../Output/FeatureVector_tfidf', 'wb') as f:
    w = csv.writer(f)
    w.writerows(feature_vector)

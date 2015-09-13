from bs4 import BeautifulSoup
import glob
import string
import math
from collections import Counter
from nltk.corpus import stopwords

allfiles = glob.glob("../DataSet/*-000.sgm")
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

tf_Idf = tf.copy()

# Counting the TF-IDF for each word
for i in tf_Idf.keys():
    art = tf_Idf[i]
    for word in art.keys():
        art[word] *= idf[word]

print tf_Idf[1]

from bs4 import BeautifulSoup
import glob
import string
import math
import csv
from newcollections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

__author__ = "Rohit Kapoor and Nandkumar Khobare"

allfiles = glob.glob("../DataSet/*000.sgm")
tags = ['places', 'title', 'dateline', 'body']
stop = stopwords.words('english')
stemmer = SnowballStemmer('english')

# To count the total number of articles
articles = 0

# Dictionary storing all the documents and word frequencies
tf = {}

# Dictionary storing all the topics with there document ID
topic_dict = {}

# List to store unique words per article to find in how many articles a word is appearing
uniqueWords = []

# A set of all topics
topic_set = set()

# Reading file and creating Term Frequencies per article
for datafile in allfiles:
    f = open(datafile, 'r')
    soup = BeautifulSoup(f.read(), "html.parser")

    for article in soup.findAll('reuters'):
        words = []
        topic = article.find('topics')
        if topic:
            topic_text = topic.get_text(' ').encode("ascii", "ignore")
            if len(topic_text) > 0:
                articles += 1
                topic_list = topic_text.split(' ')
                topic_dict[articles] = topic_list
                topic_set = topic_set.union(topic_list)
                for tag in tags:
                    text = article.find(tag)
                    if text:
                        text = text.get_text(' ').encode("ascii", "ignore")
                        final_string = text.translate(None, string.punctuation).lower()
                        filtered_words = [stemmer.stem(word) for word in final_string.split() if word not in stop]
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

# Storing most common 2048 words per article
allWords = []

# Counting the TF-IDF for each word and storing most common 2048 words in allWords
for i in tf_Idf.keys():
    art = tf_Idf[i]
    for word in art.keys():
        art[word] *= idf[word]
    allWords += art.most_common(2048)

# Sorting all the words according to TF-IDF value
allWords.sort(key=lambda tup: tup[1], reverse=True)

# Filtering out unique words
seen = set()

# List containing words with highest TF-IDF
feature_words = []

# Filtering unique words
for word, val in allWords:
    if word not in seen and word not in topic_set:
        feature_words.append(word)
        seen.add(word)

# Filtering top 2048 words
feature_words = feature_words[:2048]

# For storing the feature vector with tf-idf
feature_vector = []

# First column of the matrix representing document-id
heading = ['topic']
heading.extend(feature_words)

feature_vector.append(heading)

attribute_type = ['d'] * (len(feature_words) + 1)

feature_vector.append(attribute_type)

feature_type = ['c']

feature_vector.append(feature_type)

# Creating the feature vectors by iterating over feature words
for i in tf_Idf.keys():
    topics = topic_dict[i]
    for topic in topics:
        row = [topic]
        for word in feature_words:
            if word in tf_Idf[i]:
                row.append(1)
            else:
                row.append(0)
        feature_vector.append(row)

# Writing to the tab file which can be opened using excel
with open('../Output/FeatureVector_tfidf.tab', 'wb') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerows(feature_vector)

from bs4 import BeautifulSoup
import glob
import string
import time
import math
import csv
import Orange
from newcollections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

__author__ = "Rohit Kapoor and Nandkumar Khobare"

allfiles = glob.glob("../DataSet/*.sgm")
tags = ['places', 'title', 'body']
stop = stopwords.words('english')
stemmer = SnowballStemmer('english')

# Configuration parameters
features = 2048

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
        # Ignoring all documents with no topic
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
                        filtered_words = [stemmer.stem(word) for word in final_string.split() if word not in stop and not word.isdigit()]
                        words += filtered_words
                tf[articles] = Counter(words)
                uniqueWords += Counter(words).keys()

    print datafile + " done"

# Count of how many articles a word is appearing in
appearance = Counter(uniqueWords)

# Saving inverse document frequencies
idf = Counter()

# Counting the IDF for all the words
for word in appearance.keys():
    idf[word] = math.log10(articles / appearance[word])

# Filtering out topics from idf
for word in idf.keys():
    if word in topic_set:
        del idf[word]

# Filtering out top words with lowest idf
feature_words = [key for (key, value) in idf.most_common()[:-features:-1]]

# For storing the feature vector
feature_vector = []

# First column of the matrix representing class
heading = ['topic']
heading.extend(feature_words)

feature_vector.append(heading)

# Adding Orange attribute type
attribute_type = ['d'] * (len(feature_words) + 1)
feature_vector.append(attribute_type)

feature_type = ['c']
feature_vector.append(feature_type)

# Creating the feature vectors by iterating over feature words
for i in tf.keys():
    topics = topic_dict[i]
    for topic in topics:
        row = [topic]

        for word in feature_words:
            if word in tf[i]:
                row.append(1)
            else:
                row.append(0)
        feature_vector.append(row)

# Writing to the tab file which will be used by Orange
with open('../Output/FeatureVector.tab', 'wb') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerows(feature_vector)

file_name = '../Output/FeatureVector.tab'

# Loading the feature vector in Orange
data = Orange.data.Table(file_name)

print "Starting clustering"


def callback(km):
    print "Iteration: %d, changes: %d, score: %.4f" % (km.iteration, km.nchanges, km.score)

km = Orange.clustering.kmeans.Clustering(data, 3, minscorechange=0, inner_callback=callback)

clusters = Counter(km.clusters)

print clusters
print Orange.clustering.kmeans.score_fast_silhouette(km)

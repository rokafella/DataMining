from bs4 import BeautifulSoup
import glob
import string
import time
import math
import csv
import Orange
import random
from newcollections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

__author__ = "Rohit Kapoor and Nandkumar Khobare"

allfiles = glob.glob("../DataSet/*.sgm")
tags = ['places', 'title', 'dateline', 'body']
stop = stopwords.words('english')
stemmer = SnowballStemmer('english')

# Configuration parameters
features = 2048
features_reduced = 512
testing_percent = 20

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

# Storing most common words per article
allWords = []

# Counting the TF-IDF for each word and storing most common words in allWords
for i in tf_Idf.keys():
    art = tf_Idf[i]
    for word in art.keys():
        art[word] *= idf[word]
    allWords += art.most_common(features)

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

# Filtering top words
feature_words = feature_words[:features]

# Filtering reduced set of feature words
feature_words_reduced = feature_words[:features_reduced]

# For storing the feature vector
feature_vector = []

# For storing the reduced feature vector
feature_vector_reduced = []

# First column of the matrix representing class
heading = ['topic']
heading.extend(feature_words)

feature_vector.append(heading)

# Similar heading for reduced feature vector
heading = ['topic']
heading.extend(feature_words_reduced)

feature_vector_reduced.append(heading)

# Adding Orange attribute type
attribute_type = ['d'] * (len(feature_words) + 1)

feature_vector.append(attribute_type)

# Adding Orange attribute type for reduced feature vector
attribute_type = ['d'] * (len(feature_words_reduced) + 1)

feature_vector_reduced.append(attribute_type)

feature_type = ['c']

feature_vector.append(feature_type)
feature_vector_reduced.append(feature_type)

# Creating the feature vectors by iterating over feature words
for i in tf_Idf.keys():
    topics = topic_dict[i]
    for topic in topics:
        row = [topic]
        row_reduced = [topic]

        for word in feature_words:
            if word in tf_Idf[i]:
                row.append(1)
            else:
                row.append(0)
        feature_vector.append(row)

        for word in feature_words_reduced:
            if word in tf_Idf[i]:
                row_reduced.append(1)
            else:
                row_reduced.append(0)
        feature_vector_reduced.append(row_reduced)

# Writing to the tab file which will be used by Orange
with open('../Output/FeatureVector.tab', 'wb') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerows(feature_vector)

# Writing to the tab file which will be used by Orange
with open('../Output/FeatureVector_reduced.tab', 'wb') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerows(feature_vector_reduced)

for current_features in [features, features_reduced]:
    print "Starting classification for " + str(current_features) + " features"

    test_data_size = int((testing_percent * current_features) / 100)

    # Selecting appropriate files
    file_name = None
    if current_features == features:
        file_name = '../Output/FeatureVector.tab'
    else:
        file_name = '../Output/FeatureVector_reduced.tab'

    # Loading the feature vector in Orange
    data = Orange.data.Table(file_name)

    # Dividing testing and training data
    test = Orange.data.Table(random.sample(data, test_data_size))
    train = Orange.data.Table([d for d in data if d not in test])

    start = time.clock()
    print "Starting training: " + str(start)

    #classifier = Orange.classification.knn.kNNLearner(train)
    classifier = Orange.classification.bayes.NaiveLearner(train)

    end = time.clock()
    print "Finished training: " + str(end)
    print "Training time : " + str(end - start)

    start = time.clock()
    print "Starting testing: " + str(start)

    accurate_word_count = 0

    for d in test:
        if classifier(d) == d.getclass():
            accurate_word_count += 1

    end = time.clock()
    print "Finished testing: " + str(end)
    print "Testing time : " + str(end - start)
    print "Classification accuracy percentage : " + str(float(accurate_word_count * 100 / test_data_size))

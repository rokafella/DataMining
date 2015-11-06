from bs4 import BeautifulSoup
import glob
import string
import time
import math
import csv
import Orange
import numpy
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
topic_seq = []

# Creating the feature vectors by iterating over feature words
for i in tf.keys():
    topics = topic_dict[i]
    for topic in topics:
        row = [topic]
        topic_seq.append(topic)
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


def callback(km):
    print "Iteration: %d, changes: %d, score: %.4f" % (km.iteration, km.nchanges, km.score)


def entropy(clusters):
        container = {}

        for t, cluster in clusters:
            if cluster in container:
                container[cluster].append(t)
            else:
                container[cluster] = [t]

        entropy_final = 0.0

        for id in container.keys():
            topic_count = Counter(container[id])
            ent = 0.0
            for t in topic_count.keys():
                ent += (float(topic_count[t]) / clusters_count[id]) * math.log((float(clusters_count[id]) / topic_count[t]), 2)
            entropy_final += (float(clusters_count[id]) / len(topic_seq)) * ent
        return entropy_final

choice = input("Please select 1->Kmeans and 2->Hierarchical: ")

distance = input("Please select a distance metric 1->Euclidean and 2->Manhattan: ")

if distance == 1:
    distance = Orange.distance.Euclidean
else:
    distance = Orange.distance.Manhattan

clusters_count = {}

if choice == 1:

    print "Starting Kmeans clustering"

    start = time.clock()

    km = Orange.clustering.kmeans.Clustering(data, 77, minscorechange=0, inner_callback=callback, distance=distance)

    end = time.clock()

    print "Clustering time: " + str(end - start)

    clusters_count = Counter(km.clusters)

    print 'Silhouette: ' + str(Orange.clustering.kmeans.score_fast_silhouette(km))
    print 'Entropy: ' + str(entropy(zip(topic_seq, km.clusters)))
    print 'Variance: ' + str(numpy.var(clusters_count.values()))

else:

    linkage = input("Please select a linkage 1->Single, 2->Average, 3->Complete: ")

    if linkage == 1:
        linkage = Orange.clustering.hierarchical.SINGLE
    elif linkage == 2:
        linkage = Orange.clustering.hierarchical.AVERAGE
    else:
        linkage = Orange.clustering.hierarchical.COMPLETE

    print "Starting Hierarchical clustering"

    start = time.clock()

    matrix = Orange.distance.distance_matrix(data, distance)

    clustering = Orange.clustering.hierarchical.HierarchicalClustering()
    clustering.linkage = linkage

    root = clustering(matrix)

    root.mapping.objects = data

    end = time.clock()

    print "Clustering time: " + str(end - start)

    topmost = sorted(Orange.clustering.hierarchical.top_clusters(root, 77), key=len)

    ls_topic = []

    for n, cluster in enumerate(topmost):
        print str(n) + '--->' + str(len(cluster))
        clusters_count[n] = len(cluster)
        for inst in cluster:
            ls_topic.append((str(inst[-1]), n))

    print ls_topic
    print clusters_count
    print 'Entropy: ' + str(entropy(ls_topic))
    print 'Variance: ' + str(numpy.var(clusters_count.values()))

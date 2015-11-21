from bs4 import BeautifulSoup
import glob
import string
import time
import math
import csv
import numpy
from newcollections import Counter
from random import randint
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

__author__ = "Rohit Kapoor and Nandkumar Khobare"

PRIME = 655241
#PRIME = 341827

allfiles = glob.glob("../DataSet/*00*.sgm")
tags = ['places', 'title', 'body']
stop = stopwords.words('english')
stemmer = SnowballStemmer('english')

# To count the total number of articles
document_id = 0

# To store all shingles with their ID
shingle_dict = {}

# To store shingle IDs in every documents
shingles_per_doc = {}

# To store words per doc
words_per_doc = {}

shingle_count = 0

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
                document_id += 1
                for tag in tags:
                    text = article.find(tag)
                    if text:
                        text = text.get_text(' ').encode("ascii", "ignore")
                        final_string = text.translate(None, string.punctuation).lower()
                        filtered_words = [stemmer.stem(word) for word in final_string.split() if word not in stop and not word.isdigit()]
                        words += filtered_words

                words_per_doc[document_id] = words
                shingles_list = []

                for index, word in enumerate(words[:-2]):
                    shingle = word + " " + words[index + 1] + " " + words[index + 2]
                    shingle_id = None
                    if shingle in shingle_dict:
                        shingle_id = shingle_dict[shingle]
                    else:
                        shingle_id = shingle_count
                        shingle_dict[shingle] = shingle_id
                        shingle_count += 1
                    shingles_list.append(shingle_id)

                shingles_per_doc[document_id] = shingles_list

    print datafile + " done"


def get_jaccard(list_a, list_b):
    set_a = set(list_a)
    set_b = set(list_b)
    intersection = len(set_a.intersection(set_b))
    union = len(set_a) + len(set_b) - intersection
    if union == 0:
        return 0
    else:
        return intersection / float(union)


def get_hash(param_a, param_b, shingle_index):
    return (((param_a * shingle_index) + param_b) % PRIME) % shingle_count

print "Number of documents: " + str(document_id)
print "Number of shingles: " + str(shingle_count)
# k = input("Please enter the value of k:")

print "Generating baseline similarity"

start = time.clock()

true_jaccard = {}

for i in range(1, document_id + 1):
    true_jaccard[i] = []
    for j in range(i + 1, document_id + 1):
        true_jaccard[i].append(get_jaccard(words_per_doc[i], words_per_doc[j]))

end = time.clock()

print "Completed baseline similarity in time: " + str(end - start)

k_values = [16, 32, 64, 128, 256]

for k in k_values:
    used_a = set()
    used_b = set()

    signature_matrix = {}

    print "Generating k-minhash sketch for k = " + str(k)

    start = time.clock()

    for i in range(1, k + 1):
        a = randint(1, shingle_count)
        while a in used_a:
            a = randint(1, shingle_count)
            used_a.add(a)

        b = randint(1, shingle_count)
        while b in used_b:
            b = randint(1, shingle_count)
            used_b.add(b)

        for doc, shingles in shingles_per_doc.iteritems():
            minimum = shingle_count + 1
            for shingle in shingles:
                h = get_hash(a, b, shingle)
                if h < minimum:
                    minimum = h
            if doc in signature_matrix:
                signature_matrix[doc].append(minimum)
            else:
                signature_matrix[doc] = [minimum]

    end = time.clock()

    print "Completed k-minhash sketch in time: " + str(end - start)

    k_minhash_estimate = {}

    print "Generating jaccard estimate from k-minhash"

    start = time.clock()

    for i in range(1, document_id + 1):
        k_minhash_estimate[i] = []
        for j in range(i + 1, document_id + 1):
            k_minhash_estimate[i].append(get_jaccard(signature_matrix[i], signature_matrix[j]))

    end = time.clock()

    print "Completed jaccard estimate from k-minhash for k = " + str(k) + " in time: " + str(end - start)

    comparisons = 0
    square_error = 0

    for i, val in k_minhash_estimate.iteritems():
        true_sim = true_jaccard[i]
        for idx, estimate in enumerate(val):
            comparisons += 1
            square_error += (true_sim[idx] - estimate)**2

    print "Number of comparisons: " + str(comparisons)
    print "Mean squared error: " + str(square_error / comparisons)

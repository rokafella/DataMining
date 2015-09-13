from bs4 import BeautifulSoup
import glob
import string
from collections import Counter
from nltk.corpus import stopwords

allfiles = glob.glob("../DataSet/*-000.sgm")
tags = ['topics', 'places', 'title', 'dateline', 'body']
stop = stopwords.words('english')

articles = 0

# Dictionary storing all the documents and word frequencies
allArticles = {}

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
        allArticles[articles] = Counter(words)
        uniqueWords += allArticles[articles].keys()

    print datafile + " done"

print Counter(uniqueWords)
from bs4 import BeautifulSoup
import glob
import string
import nltk
from collections import Counter
from nltk.corpus import stopwords

allfiles = glob.glob("../DataSet/*.sgm")
tags = ['topics', 'places', 'title', 'dateline', 'body']
stop = stopwords.words('english')

total = 0

words = []

for datafile in allfiles:
    f = open(datafile, 'r')
    soup = BeautifulSoup(f.read(), "html.parser")

    for article in soup.findAll('reuters'):
        for tag in tags:
            text = article.find(tag)
            if text:
                text = text.text.encode("ascii", "ignore")
                final_string = text.translate(None, string.punctuation).lower()
                filtered_words = [word for word in final_string.split() if word not in stop]
                words += filtered_words
                total += len(filtered_words)

    print datafile + " done"

print str(total) + " words"
tokens = nltk.word_tokenize(' '.join(words))
print Counter(tokens).most_common(10)

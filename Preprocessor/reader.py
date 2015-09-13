from bs4 import BeautifulSoup
import glob
import xml.etree.ElementTree as eT
import string
from nltk.corpus import stopwords

allfiles = glob.glob("../DataSet/*.sgm")
tags = ['topics', 'places', 'title', 'dateline', 'body']
stop = stopwords.words('english')


def remove_tags(text):
    return ' '.join(eT.fromstring(text).itertext())

total = 0

for datafile in allfiles:
    f = open(datafile, 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')

    for tag in tags:
        collections = soup.findAll(tag)
        for collection in collections:
            plain_string = remove_tags(str(collection).replace('', ''))
            final_string = plain_string.translate(string.maketrans('', ''), string.punctuation).lower()
            filtered_words = [word for word in final_string.split() if word not in stop]

            total += len(filtered_words)

    print datafile + " done"

print total

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

for datafile in allfiles:
    f = open(datafile, 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    for tag in tags:
        collections = soup.findAll(tag)
        plain_string = remove_tags(str(collections[0]).replace('', ''))
        final_string = plain_string.translate(string.maketrans('', ''), string.punctuation).lower()
        filtered_words = [word for word in final_string.split() if word not in stop]
        print filtered_words
# f = open('../DataSet/reut2-000.sgm', 'r')
# data = f.read()
# soup = BeautifulSoup(data, 'html.parser')
# bodies = soup.findAll('body')
# for body in bodies:
#     words = str(body)[6:-9].split()
#     print words[0]
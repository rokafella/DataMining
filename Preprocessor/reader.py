from bs4 import BeautifulSoup
import glob
import xml.etree.ElementTree as eT
import string
from nltk.corpus import stopwords

allfiles = glob.glob("../DataSet/*.sgm")
tags = ['topics', 'places', 'title', 'dateline', 'body']
stop = stopwords.words('english')
word_frequency = {}


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

        for filtered_word in filtered_words:
            if filtered_word in word_frequency.keys():
                word_frequency[filtered_word] += 1
            else:
                word_frequency[filtered_word] = 1

print("Word frequencies are : ")
print(word_frequency)
word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
print("Word frequencies in descending order are : ")
print(word_frequency)

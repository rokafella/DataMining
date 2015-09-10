from bs4 import BeautifulSoup
import glob
import xml.etree.ElementTree as eT
import string

allfiles = glob.glob("../DataSet/*.sgm")
tags = ['topics', 'places', 'title', 'dateline', 'body']


def remove_tags(text):
    return ' '.join(eT.fromstring(text).itertext())

for datafile in allfiles:
    f = open(datafile, 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    for tag in tags:
        collections = soup.findAll(tag)
        plain_string = remove_tags(str(collections[0]).replace('', ''))
        final_string = plain_string.translate(string.maketrans('', ''), string.punctuation)
        print final_string
# f = open('../DataSet/reut2-000.sgm', 'r')
# data = f.read()
# soup = BeautifulSoup(data, 'html.parser')
# bodies = soup.findAll('body')
# for body in bodies:
#     words = str(body)[6:-9].split()
#     print words[0]
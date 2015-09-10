from bs4 import BeautifulSoup
import glob
import xml.etree.ElementTree as eT

allfiles = glob.glob("../DataSet/*.sgm")
tags = ['body']


def remove_tags(text):
    return ' '.join(eT.fromstring(text).itertext())

for datafile in allfiles[:1]:
    f = open(datafile, 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    for tag in tags:
        collections = soup.findAll(tag)
        print str(collections[0]).replace('', '')
        print remove_tags(str(collections[0]).replace('', ''))
# f = open('../DataSet/reut2-000.sgm', 'r')
# data = f.read()
# soup = BeautifulSoup(data, 'html.parser')
# bodies = soup.findAll('body')
# for body in bodies:
#     words = str(body)[6:-9].split()
#     print words[0]
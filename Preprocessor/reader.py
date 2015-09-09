from bs4 import BeautifulSoup

f = open('../DataSet/reut2-000.sgm', 'r')
data = f.read()
soup = BeautifulSoup(data, 'html.parser')
bodies = soup.findAll('body')
print len(bodies)
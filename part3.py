import requests
from bs4 import BeautifulSoup

print('\n*********** PART 2 ***********')
print('Michigan Daily -- MOST READ\n')

baseurl = 'https://www.michigandaily.com/'
page_text = requests.get(baseurl).text
page_soup = BeautifulSoup(page_text, 'html.parser')

most_read_contents = page_soup.find(class_='view-most-read')
most_read_headlines = most_read_contents.find_all('li')

headline_lst=[]
for headline in most_read_headlines:
	headline_lst.append(headline.string)

link_lst=[]
for link in most_read_contents.find_all('a'):
	link_lst.append('https://www.michigandaily.com'+link.get('href'))

author_lst=[]
for link in link_lst:
	article_page_text=requests.get(link).text
	article_soup = BeautifulSoup(article_page_text,'html.parser')
	author = article_soup.find('div',class_="byline")
	if (author != None):
		author_string = author.next_element.next_element.next_element.string
		author_lst.append(author_string)
	else:
		author_lst.append("BY DAILY STAFF WRITER")

def output():
	i = 0
	while (i < len(author_lst)):
		print(headline_lst[i])
		print("   by " + author_lst[i])
		i = i + 1

output()

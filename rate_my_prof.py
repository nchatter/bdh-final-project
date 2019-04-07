import requests
import json
import math
import pandas as pd
from bs4 import BeautifulSoup
import re

class Scraper:
	def __init__(self, university):
		self.univ_id = university
		self.profs = self.getAllProfs()

	def getAllProfs(self):
		numProfs = self.findNumProfs(self.univ_id)
		totPages = math.ceil(numProfs / 20)
		ind = 1
		listOfProfs = []
		while (ind <= totPages):
			url = "http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
					ind) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(self.univ_id)
			requestPage = requests.get(url)
			page = json.loads(requestPage.content)
			listOfProfs.extend(page['professors'])
			ind += 1
		return listOfProfs

	def findNumProfs(self, univ_id):
		page = requests.get(
                "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                    univ_id))
		jsonPage = json.loads(page.content)
		numProfs = jsonPage['remaining'] + 20
		return numProfs

	def getProfComments(self, tid):
		page = requests.get(
				"https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(tid))
		soup = BeautifulSoup(page.text, 'html.parser')
		comments = soup.find_all("p", class_="commentsParagraph")
		return comments

GATech = Scraper(361)
gatechProfs = GATech.getAllProfs()
# comments = GATech.getProfComments(2356565)
profComments = dict()
for prof in gatechProfs:
	comments = GATech.getProfComments(prof['tid'])
	profComments[prof['tid']] = comments

profs = pd.DataFrame(gatechProfs)
profs.to_csv('profs.csv')

for tid in profComments:
	print(tid)
	print(profComments[tid])
	print(len(profComments[tid]))
comments = pd.DataFrame.from_dict(profComments)
comments.to_csv('comments.csv')





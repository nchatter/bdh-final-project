import requests
import json
import math
import pandas as pd

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

GATech = Scraper(361)

gatechProfs = GATech.getAllProfs()
print(gatechProfs)

df = pd.DataFrame(gatechProfs)
df.to_csv('profs.csv')

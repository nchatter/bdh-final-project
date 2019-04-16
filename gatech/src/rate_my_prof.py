# Scraper for Rate My Professor website

import requests
import json
import math
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from sentiment import text_to_pos_sentiment_score

class Scraper:
	def __init__(self, university):
		self.univ_id = university
		self.profs = self.getAllProfs()

	# function that gets all professors for the chosen university
	# goes through all possible pages
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

	# function that finds the total number of professors
	# used to calculate the number of pages that will be present
	def findNumProfs(self, univ_id):
		page = requests.get(
                "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                    univ_id))
		jsonPage = json.loads(page.content)
		numProfs = jsonPage['remaining'] + 20
		return numProfs

	# function that collects all the comments for a given professor id
	def getProfComments(self, tid):
		page = requests.get(
				"https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(tid))
		soup = BeautifulSoup(page.text, 'html.parser')
		all_comments = soup.find_all("p", class_="commentsParagraph")
		comments = []
		for comment in all_comments:
			comments.append(str(comment))
		return comments

# initialize the scraper
GATech = Scraper(361)

# obtain and parse the comments
gatechProfs = GATech.getAllProfs()
profComments = dict()
for prof in gatechProfs:
	comments = GATech.getProfComments(prof['tid'])
	cleaned_comments = []
	for comment in comments:
		first_close = comment.find(">")
		comment = comment[first_close + 1:]
		second_open = comment.find("<")
		clean_comment = comment[:second_open].strip()
		cleaned_comments.append(clean_comment)
	profComments[prof['tid']] = cleaned_comments

# creating the CSV with professor data
profs = pd.DataFrame(gatechProfs)
profs.to_csv('../data/prof_data/profs.csv')

prof_rating = {}
for tid in profComments:
		if (profComments[tid] and (profComments[tid] != 1848155)):
			prof_rating[tid] = text_to_pos_sentiment_score(''.join(comment for comment in profComments[tid]))
		else:
			prof_rating[tid] = 0

with open('../data/prof_data/rating.csv', 'a') as fp:
	w = csv.writer(fp)
	w.writerows(prof_rating.items())



import requests
import json
import math
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from sentiment import text_to_pos_sentiment_score
import sys

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
		all_comments = soup.find_all("p", class_="commentsParagraph")
		comments = []
		for comment in all_comments:
			comments.append(str(comment))
		return comments

startIdx = int(sys.argv[1])
endIdx = int(sys.argv[2])

UIUC = Scraper(1112)
UIUCprofs = UIUC.getAllProfs()
# comments = GATech.getProfComments(2356565)
for prof in UIUCprofs[startIdx:endIdx]:
	comments = UIUC.getProfComments(prof['tid'])
	cleaned_comments = []
	score = 0
	count = 0
	for comment in comments:
		first_close = comment.find(">")
		comment = comment[first_close + 1:]
		second_open = comment.find("<")
		clean_comment = comment[:second_open].strip().decode('utf-8').encode('ascii', 'ignore').decode('unicode_escape')
		if clean_comment:
			score += text_to_pos_sentiment_score(clean_comment)
			count += 1
		cleaned_comments.append(clean_comment)
	prof_data = [prof['tid'],prof['overall_rating'],prof['tFname'],prof['tLname'],prof['tNumRatings']]
	if count > 0:
		prof_data.append(float(score)/count)
	else:
		prof_data.append(0)
	prof_data.extend(cleaned_comments)
	with open("../data/prof_data/prof_comments_score_" + str(startIdx) + "_" + str(endIdx) + ".csv", "a") as fp:
		wr = csv.writer(fp)
		try:
			wr.writerow(prof_data)
			print(prof_data[0:6])
		except:
			pass



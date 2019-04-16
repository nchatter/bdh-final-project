import requests
import re
import os
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd

def getSubjects(url, year, term):
    url += str(year) + '/' + term + '.xml'
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    subjects = soup.find_all("subject",attrs={"id":True})
    subject_url_map = {}
    for subject in subjects:
        subject_url_map[subject.attrs['id']] = subject.attrs['href']
    return subject_url_map

def getCourses(url,subject_id):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    courses = soup.find_all("course",attrs={"id":True})
    course_url_map = {}
    for course in courses:
        course_url_map[course.attrs['id']] = course.attrs['href'][0:-3] + "html"
    return course_url_map

def getCourseDetails(course_url,prefix):
    response = requests.get(course_url)
    soup = BeautifulSoup(response.text)

    credits = soup.find_all('p', attrs={"class":"padtop10"})[0]
    credits = credits.text.split(":")[1].strip().split(' ')[0]
    prefix.append(credits)

    data = []
    table = soup.find('table', attrs={'class': 'tablesorter'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr', attrs={"class":False})
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip().encode('ascii', 'ignore').decode('unicode_escape') for ele in cols]
        if 'Lecture' in cols[2]:
            print(prefix + cols)
            data.append(prefix + cols)
    return data



if __name__ == '__main__':
    years = [2018, 2017, 2016, 2015]
    semesters = ['fall', 'spring']
    #semesters = ['spring']
    url = "https://courses.illinois.edu/cisapp/explorer/schedule/"
    data = []
    for year in years:
        for term in semesters:
            subjects_url_map = getSubjects(url, year, term)
            for subject in subjects_url_map:
                courses_url_map = getCourses(subjects_url_map[subject], subject)
                for key in courses_url_map:
                    prefix = [year, term, subject, key]
                    course_data = getCourseDetails(courses_url_map[key],prefix)
                    data.extend(course_data)
    df = pd.DataFrame(data)
    df.to_csv('../data/course_data/uiuc_combined_data.csv', sep=',')




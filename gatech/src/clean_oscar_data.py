import csv
import os
import pandas as pd
import numpy as np

if __name__ == '__main__':
    oscar_data = []
    course_names_set = set()

    path = "oscar_data/"
    for item in os.listdir(path):
        with open(path + item) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            term = item.split('_')[2]
            for row in readCSV:
                if "Lecture" in row[11]:
                    course_name = row[0][2:-2]
                    course_crn = row[1]
                    course_num = row[2]
                    course_section = row[3]
                    course_credits = row[4]
                    course_time = row[8]
                    course_prof = row[12]
                    new_row = [term,course_name,course_crn,course_num,course_section,course_credits,course_time,course_prof]
                    oscar_data.append(new_row)

    dataframe = pd.DataFrame(oscar_data)
    dataframe.to_csv('combined_oscar_data.csv', sep=',')





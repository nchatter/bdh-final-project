import csv
import os
import pandas as pd
import numpy as np

def getNumCount(course_name):
    return sum(c.isdigit() for c in course_name)

def checkHeader(row):
    header = ''.join(elem for elem in row)
    return 'ABCD' in header


if __name__ == '__main__':
    irp_data = []
    course_names_set = set()

    path = "irp_data/"
    for item in os.listdir(path):
        with open(path + item) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                term = item.split('_')[1].split('.')[0]
                course_num_section = row[0]
                number_count = getNumCount(course_num_section)
                header_check = checkHeader(row)
                if number_count >= 4 and (course_num_section not in course_names_set) and not header_check:
                    course_num_section_split = row[0].split('-')
                    course_num = ' '.join(elem for elem in course_num_section_split[1].strip().split(' ')[0:-1])
                    course_section = course_num_section_split[1].strip().split(' ')[-1]
                    last_col = row[-1]
                    data = last_col.split()
                    if len(data) == 3:
                        withdraw = data[0]
                        gpa = data[1]
                        enrollment = data[2]
                        new_row = [term, course_num, course_section, gpa, enrollment]
                        irp_data.append(new_row)
                        course_names_set.add(term + course_num + course_section)
                    elif len(data) == 2:
                        withdraw = 0
                        gpa = data[0]
                        enrollment = data[1]
                        new_row = [term, course_num, course_section, gpa, enrollment]
                        irp_data.append(new_row)
                        course_names_set.add(term + course_num + course_section)
    dataframe = pd.DataFrame(irp_data)
    dataframe.to_csv('combined_irp_data.csv', sep=',')


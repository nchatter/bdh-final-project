import requests
import re
import os
from bs4 import BeautifulSoup
import json
import csv
from time import time
from time import sleep

def get_subject_html(term_id, sel_subject):
    course_url_base = 'https://oscar.gatech.edu/pls/bprod/bwckschd.p_get_crse_unsec?term_in='
    course_url_mid = '&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj='
    course_url_end = '&sel_crse=&sel_title=&sel_schd=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'

    url = course_url_base + term_id + course_url_mid + sel_subject + course_url_end
    html = requests.get(url).text

    file = open(term_id + "/" + term_id + "_" + sel_subject + ".html", "w")
    file.write(html)
    file.close()

def get_subjects(term_id):
    subject_url = 'https://oscar.gatech.edu/pls/bprod/' + 'bwckgens.p_proc_term_date'
    subject_params = {'p_calling_proc':'bwckschd.p_disp_dyn_sched',
                      'p_term':term_id}
    subject_url = "https://oscar.gatech.edu/pls/bprod/bwckgens.p_proc_term_date?p_calling_proc=bwckschd.p_disp_dyn_sched&p_term=" + term_id
    html = requests.get(subject_url, params=subject_params).text


    soup = BeautifulSoup(html,features='html.parser')
    select = soup.find('select', {'id': 'subj_id'})
    options = select.findAll('option')
    out = []
    for option in options:
        attrs = dict(option.attrs)
        out.append((attrs['value'],option.text))
    return out

def get_dddefault_count(lines):
    count = 0
    next_course = False
    for line in lines:
        if 'dddefault' in line:
            count += 1
        if 'ddtitle' in line or 'Return to Previous' in line:
            return count, True
    return count, next_course

def get_enrollment_numbers(course_link):
    html = requests.get(course_link).text.splitlines()
    line_count = 0
    three_line_chunk = html[line_count:line_count+3]
    num_dddefault, _ = get_dddefault_count(three_line_chunk)
    while num_dddefault < 3 and line_count < len(html):
        line_count += 1
        three_line_chunk = html[line_count:line_count + 3]
        num_dddefault, _ = get_dddefault_count(three_line_chunk)
    index1 = three_line_chunk[0].find('">') + 2
    capacity = three_line_chunk[0][index1:three_line_chunk[0].find('</td')]
    actual = three_line_chunk[1][index1:three_line_chunk[1].find('</td')]
    return capacity,actual

def get_courses(directory):
    courses = []
    ignore_count = 0
    process_count = 0

    files = os.listdir(directory)
    for file in files:
        if directory[0:len(directory)-1] in file:
            current_file = os.path.join(directory, file)

            with open(current_file) as f:
                html = f.readlines()
            line_count = 0

            while line_count < len(html):
                line = html[line_count]
                if 'ddtitle' in line:
                    crn_index = line.find('crn_in=')
                    link_start_address = line.find('href="') + 6
                    link_end_index = line.find('&amp')

                    course_link = 'https://oscar.gatech.edu' + line[link_start_address:link_end_index]

                    carrot_close_index = crn_index + 13
                    line = line[carrot_close_index + 1:]
                    carrot_open_index = line.find('<')
                    text = re.split(' - ',line[0:carrot_open_index])
                    course_name = text[0:-3]
                    course_crn = text[-3].strip()
                    course_number = text[-2].strip()
                    course_section = text[-1].strip()

                    course_link += '&crn_in=' + course_crn
                    print(course_number)

                    line_count += 1
                    credit_hours = 0
                    while credit_hours == 0:
                        line = html[line_count]
                        if 'Credits' in line:
                            credit_hours = line.strip().split(' ')[-2]
                        line_count += 1

                    seven_line_chunk = html[line_count:line_count+7]
                    num_dddefault, next_course =  get_dddefault_count(seven_line_chunk)
                    while num_dddefault < 7 and (not next_course) and (line_count < len(html)):
                        line_count += 1
                        seven_line_chunk = html[line_count:line_count+7]
                        num_dddefault, next_course = get_dddefault_count(seven_line_chunk)

                    if not next_course:
                        capacity, actual = get_enrollment_numbers(course_link)
                        index1 = seven_line_chunk[0].find('">')+2
                        type = seven_line_chunk[0][index1:seven_line_chunk[0].find('</td')]
                        time = seven_line_chunk[1][index1:seven_line_chunk[1].find('</td')]
                        days = seven_line_chunk[2][index1:seven_line_chunk[2].find('</td')]
                        where = seven_line_chunk[3][index1:seven_line_chunk[3].find('</td')]
                        schedule_type = seven_line_chunk[5][index1:seven_line_chunk[5].find('</td')]
                        instructor = seven_line_chunk[6][index1:seven_line_chunk[6].find('(<ABBR')]
                        process_count += 1

                        course = (course_name, course_crn, course_number, course_section, credit_hours, capacity, actual, type, time, days, where, schedule_type, instructor)
                        courses.append(course)

                    else:
                        ignore_count += 1



                line_count += 1

    return courses, ignore_count, process_count




if __name__ == '__main__':

    term_ids = ['201808','201805','201802','201708','201705','201702','201608','201605','201602','201508','201505','201502', '201408','201405','201402']
    '''
    for term in term_ids:
        subjects = get_subjects(term)
        for abv,name in subjects:
            get_subject_html(term, abv)
    '''
    all_courses = []
    ignore = 0
    process = 0

    start = time()
    term = '201402'
    directory = term + '/'
    term_sem_courses, ignore_count, process_count = get_courses(directory)
    all_courses.extend(term_sem_courses)
    ignore += ignore_count
    process += process_count
    with open('oscar_data_' + term, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for tup in term_sem_courses:
            writer.writerow(tup)


    data = {'ignore':ignore, 'process':process}
    with open('process_' + term + '.json', 'w') as fp:
        json.dump(data, fp)
    end = time()
    print(end - start)

    '''
    with open('oscar_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for tup in all_courses:
            writer.writerow(tup)
    '''







import requests
import json
import csv
import numpy as np
import pandas as pd
from IPython.display import display
import time
import sys


def text_to_pos_sentiment_score(text):
    url = 'http://text-processing.com/api/sentiment/'
    data = 'text={0}'.format(text)
    response = requests.post(url, data=data)
    json_data = json.loads(response.text)
    return json_data["probability"]["pos"]


def text_to_sentiment_label(text):
    url = 'http://text-processing.com/api/sentiment/'
    data = 'text={0}'.format(text)
    response = requests.post(url, data=data)
    json_data = json.loads(response.text)
    return json_data["label"]


def create_sentiment_table(file_in, file_out):
    with open(file_out, 'w') as f_out:
        out_colnames = ['Professor', 'Quality', 'Difficulty', 'Class', 'Comments', 'Positve Sentiment Score', 'Label']
        out_writer = csv.DictWriter(f_out, fieldnames=out_colnames, lineterminator='\n')
        out_writer.writeheader()

        with open(file_in) as f_in:
            in_reader = csv.DictReader(f_in)
            for row in in_reader:
                row_value_list = [row['Professor'], row['Quality'], row['Difficulty'], row['Class'], row['Comments'],
                                  text_to_pos_sentiment_score(row['Comments']),
                                  text_to_sentiment_label(row['Comments'])]
                new_point = dict(zip(out_colnames, row_value_list))
                out_writer.writerow(new_point)

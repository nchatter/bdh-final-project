# Big Data For Health Final Project
This documentation is written in markdown grammar. To gain better reading experience, use an editor that supports markdown. You can also read it on our project github page: [CSE 6250 Project](https://github.com/nchatter/bdh-final-project)

## Overview
This project is about understanding correlations between factors institutes can control in student success, as measured by GPA. 
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Data Collection](#data-collection)
- [Data Filtering and Cleaning](#data-filtering)
- [Data Aggregation](#data-aggregation)
- [Model](#model)
- [Authors](#authors)

## Prerequisites
This project is written in Python and Apache Hive, providing scripts which collect, process, and evaluate data. Make sure that your environment supprot Hadoop before you run the hive script. You can install the environment locally following the instruction: 
[Docker in local OS](http://www.sunlab.org/teaching/cse6250/spring2019/env/env-local-docker.html#_1-install-docker).

We use Python 3 for this project. You need the following packages:
```python
requests==2.18.4 
pandas==0.22.0      
numpy==1.14.2      
matplotlib==2.2.4         
scikit-learn==0.20.3        
bs4==0.0.4     
ipython==5.8.0
```      
To install all the required packages, copy the above paragraph into a txt file `requirements.txt` and run:
```python
pip install -U -r requirements.txt
```
## Getting Started
You can directly use the project folder or clone it from the github:
```python
git clone https://github.com/nchatter/bdh-final-project.git
```
The directory includes raw data, but you can execute the scripts to regnerate the data (in case of any updates)

## Data Collection
The first aspect of this project is collecting data. There are three aspects of data that are collected for each institute: course data, grade data, and professor sentiment data. 

For Georgia Tech, the course data is pulled from Oscar, which is a part of Georgia Tech's registration system. The `pull_oscar_data.py` script will produce a csv file for the semester that the script is pull data for. For example, currently, the script is set to pull data for `201702` (Line 153), which translates to Spring 2017. Line 153 needs to be modified to pull data for each semester. Fall 2017 is represented at 201708 and Summer 2017 is represented as 201705. The produced csv files will be stored in the `/data/oscar_data directory`. Using the `clean_oscar_data.py` script, all of the individual course data files will be combined to produce one combined csv, called combined_oscar_data.csv. 
```python
#modify line 153 for desired semester
python pull_oscar_data.py
python clean_oscar_data.py
```
The Georgia Tech grade distribution data is a bit more challenging to collect. Due to release restrictions, the data, for each semester, first needs to be pulled in PDF files from [IRP](https://tableau.gatech.edu/#/site/IRP/views/GradeDistribution/ByClass?:iid=1). Once the PDF files are downloaded, they are sent through [Tabula](https://tabula.technology/), an open source OCR engine. The generated csv are in the `data/irp_data` directory and are combined using the `clean_irp_data.py` script which produces one combined csv for all grade data, called `combined_irp_data.csv`. 

For University of Illinois Urbana-Champaign (UIUC), course data can be pulled with the `pull_course_data.py` script which uses the universities [Course Exproler API](https://courses.illinois.edu/cisdocs/). This script pulls all course data for UIUC, and produces `uiuc_combined_data.csv` stored in the `data/course_data/` directory. 

The UIUC grade distribution is already aggregated and is publically avalible [here](https://github.com/wadefagen/datasets/tree/master/gpa). 

Professor sentiment for both universities is collected by first pulling comments from [RateMyProfessor](https://www.ratemyprofessors.com/) and then running the comments through [NLTK](http://text-processing.com) sentiment analyzing API. 

CAUTION: Running data collection scripts will take hours, run at your own risk. Cleaned data is already available in repository. 

## Data Filtering and Cleaning 
There are certain filtering operations required before merging the various datasets. 
For Georgia Tech grade data, there are certain issues when working with PDFs and an OCR library. Due to issues with how data is pulled there are certain courses where the course number is cut off. In this situation, courses are dropped. Likewise courses without a professor listed are also dropped. Below are additional filtering operations: 
- Obscure GPAs are dropped (GPA below 0.5 or above 4.00)
- Course starting times are extracted and converted to military time 
- First name of the professor is extracted 
- Last Name of the professor is extracted
- Level of the course is extracted 
- Course Department is converted to a number 

For UIUC, similar filtering operations are required: 
- Average GPA is computed 
- Courses without professor listed are dropped 
- Course starting times are extracted and converted to military time 
- First name of the professor is extracted 
- Last Name of the professor is extracted
- Level of the course is extracted 
- Course Department is converted to a number

For UIUC, one additional filtering problem occurred. Course data only includes Lectures, however, grade data is broken down by Recitation section. For example, a course like ACCTY 201 has 2 lecture sections but 18 recitation sections. Therefore, in the course data there are only two entries, but in the grade data has 18 entries. Moreover, additional difficulty arises because a student in the first lecture can attend the first recitation and a student in the second lecture could also attend the first recitation. Therefore, to account for this courses where the number of course data entries is equivalent to grade data entries are processed. 

## Data Aggregation
Once data is cleaned, the different data sources can be combined. Georgia Tech course and grade data are inner joined on term, course number, and section. UIUC course and grade data are inner joined on year, term, subject, course number, and rank. Rank is a pre-computed number that used to distinguish different sections of the same course. Professor data is aggregated using the first and last name of the professor. 

## Model 
The trainable parameters are course start time, course level, course enrollment, course department/subject, number of credits, and professor sentiment. The measured value is the GPA of the course. Of the various models tested, the best performing model is a Random Forest Regressor model. The `my_model.py` and `uiuc_model.py` show the R<sup>2</sup> value of the regression model as well as an average distance score. This distance is the average difference between predicted value and true value. Lastly, the model also produces a graph for feature importance. The best models are saved as pickle files in the corresponding src folders, but were too large to upload to Github.

## Authors
- [Nupur Chatterji](https://www.linkedin.com/in/nupurchatterji/)
- [Reshav Sain](https://www.linkedin.com/in/ssain/) 
- [Sreeramamurthy Tripuramallu](https://www.linkedin.com/in/sree-tripuramallu/) 

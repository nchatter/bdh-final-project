# Big Data For Health Final Project
This documentation is written in markdown grammar. To gain better reading experience, use an editor supports markdown. You can also read it on our project github page: [CSE 6250 Project](https://github.com/nchatter/bdh-final-project)

## Overview
This project is about understanding correlations between factors institutes can control in student success, as measured by GPA. 
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Data Collection](#data-collection)
- [Model](#model)
- [Authors](#authors)

## Prerequisites
This project is written in Apache Hive and Python, providing scripts which collect, process, and evaluate data. Make sure that your environment supprot Hadoop before you run the hive script. You can install the environment locally following the instruction: 
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

    git clone https://github.com/nchatter/bdh-final-project.git
The directory includes raw data, but you can execute the scripts to regnerate the data (in case of any updates)

## Data Collection
The first aspect of this project is collecting data. There are three aspects of data that are collected for each institute: course data, grade data, and professor sentiment data. 

For Georgia Tech, the course data is pulled from Oscar, which is a part of Georgia Tech's registration system. The `pull_oscar_data.py` script will produce a csv file for the semester that the script is pull data for. For example, currently, the script is set to pull data for `201702` (Line 153), which translates to Spring 2017. Line 153 needs to be modified to pull data for each semester. Fall 2017 is represented at 201708 and Summer 2018 is represented as 201705. The produced csv files will be stored in the `/data/oscar_data directory`. Using the `clean_oscar_data.py` script, all of the individual course data files will be combined to produce one combined csv, called combined_oscar_data.csv. 
```python
	#modify line 153 for desired semester
	python pull_oscar_data.py
	python clean_oscar_data.py
```
The Georgia Tech grade distribution data is a bit more challenging to collect. Due to release restrictions, the data, for each semester, first needs to be pulled in PDF files from [IRP](https://tableau.gatech.edu/#/site/IRP/views/GradeDistribution/ByClass?:iid=1) Once the PDF files are downloaded, they are sent through [Tabula](https://tabula.technology/),an open source OCR engine. The generated csv are in the `data/irp_data` directory and are combined using the `clean_irp_data.py` script which produces one combined csv for all grade data, called `combined_irp_data.csv`. 

## Authors
- [Nupur Chatterji](https://www.linkedin.com/in/nupurchatterji/)
- [Reshav Sain](https://www.linkedin.com/in/ssain/) 
- [Sreeramamurthy Tripuramallu](https://www.linkedin.com/in/sree-tripuramallu/) 

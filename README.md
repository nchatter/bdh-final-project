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

    requests==2.18.4 
    pandas==0.22.0      
    numpy==1.14.2      
    matplotlib==2.2.4         
    scikit-learn==0.20.3        
    bs4==0.0.4     
    ipython==5.8.0      
To install all the required packages, copy the above paragraph into a txt file `requirements.txt` and run:

    pip install -U -r requirements.txt

## Getting Started
You can directly use the project folder or clone it from the github:

    git clone https://github.com/nchatter/bdh-final-project.git
The directory includes raw data, but you can execute the scripts to regnerate the data (in case of any updates)

## Data Collection

## Authors
- [Nupur Chatterji](https://github.com/nchatter)
- [Reshav Sain](https://github.com/seanrsain) 
- [Sreeramamurthy Tripuramallu](https://github.com/stripuramallu3) 

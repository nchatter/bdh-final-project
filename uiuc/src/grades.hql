-- ***************************************************************************
-- DO NOT modify the below provided framework and variable names/orders please
-- Loading Data:
-- create external table mapping for course_gpa_data.csv

-- IMPORTANT NOTES:
-- You need to put course_gpa_data.csv under hdfs directory 
-- '/input/events/course_gpa_data.csv'
-- 
-- To do this, run the following commands for events.csv, 
-- 1. sudo su - hdfs
-- 2. hdfs dfs -mkdir -p /input/courseGPA
-- 3. hdfs dfs -chown -R root /input
-- 4. exit 
-- 5. hdfs dfs -put /path-to-course_gpa_data.csv /input/courseGPA/
-- ***************************************************************************

-- create courseGPA events table 
DROP TABLE IF EXISTS courseGPA;
CREATE EXTERNAL TABLE courseGPA (
  year INT,
  term STRING,
  subject STRING,
  number INT,
  enrollment INT,
  gpa FLOAT,
  fname STRING,
  lname STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/input/courseGPA';



INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_class'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT subject, number, avg(gpa), min(gpa), max(gpa), avg(enrollment), min(enrollment), max(enrollment)
FROM courseGPA
GROUP BY subject, number;


INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_dept'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT subject, avg(gpa), min(gpa), max(gpa)
FROM courseGPA
GROUP BY subject;


INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_term'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT year, term, avg(gpa), min(gpa), max(gpa), avg(enrollment), min(enrollment), max(enrollment)
FROM courseGPA
GROUP BY year, term;
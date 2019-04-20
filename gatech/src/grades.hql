-- ***************************************************************************
-- DO NOT modify the below provided framework and variable names/orders please
-- Loading Data:
-- create external table mapping for events.csv and mortality_events.csv

-- IMPORTANT NOTES:
-- You need to put events.csv and mortality.csv under hdfs directory 
-- '/input/events/events.csv' and '/input/mortality/mortality.csv'
-- 
-- To do this, run the following commands for events.csv, 
-- 1. sudo su - hdfs
-- 2. hdfs dfs -mkdir -p /input/events
-- 3. hdfs dfs -chown -R root /input
-- 4. exit 
-- 5. hdfs dfs -put /path-to-events.csv /input/events/
-- Follow the same steps 1 - 5 for mortality.csv, except that the path should be 
-- '/input/mortality'
-- ***************************************************************************
-- create oscar table 
DROP TABLE IF EXISTS oscar;
CREATE EXTERNAL TABLE oscar (
  index INT,
  term INT,
  name STRING,
  crn INT,
  course_num STRING,
  section STRING,
  credits FLOAT,
  time STRING,
  prof STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/input/oscar';

-- create irp events table 
DROP TABLE IF EXISTS irp;
CREATE EXTERNAL TABLE irp (
  index INT,
  term INT,
  course_num STRING,
  section STRING,
  gpa FLOAT,
  enrollment INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/input/irp';



INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_class'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT course_num, avg(gpa), min(gpa), max(gpa), avg(enrollment), min(enrollment), max(enrollment)
FROM irp
GROUP BY irp.course_num;


INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_term'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT course_num, avg(gpa), min(gpa), max(gpa), avg(enrollment), min(enrollment), max(enrollment)
FROM irp
GROUP BY irp.term;





INSERT OVERWRITE LOCAL DIRECTORY 'classes_per_semester'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT avg(event_count), min(event_count), max(event_count)
-- ***** your code below *****

FROM
(SELECT COUNT(irp.index) as event_count
FROM irp
GROUP BY irp.term) classes_per_semester;




INSERT OVERWRITE LOCAL DIRECTORY 'sections_per_class'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT avg(event_count), min(event_count), max(event_count)
-- ***** your code below *****

FROM
(SELECT COUNT(irp.section) as event_count
FROM irp
GROUP BY irp.course_num) sections_per_class;
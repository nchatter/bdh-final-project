-- ***************************************************************************
-- DO NOT modify the below provided framework and variable names/orders please
-- Loading Data:
-- create external table mapping for combined_irp_data.csv and course_irp_merged_data.csv

-- IMPORTANT NOTES:
-- You need to put combined_irp_data.csv and course_irp_merged_data.csv under hdfs directory 
-- '/input/irp/combined_irp_data.csv' and '/input/irpMerged/course_irp_merged_data.csv'
-- 
-- To do this, run the following commands for events.csv, 
-- 1. sudo su - hdfs
-- 2. hdfs dfs -mkdir -p /input/irp
-- 3. hdfs dfs -chown -R root /input
-- 4. exit 
-- 5. hdfs dfs -put /path-to-irp.csv /input/irp/
-- Follow the same steps 1 - 5 for course_irp_merged_data.csv, except that the path should be 
-- '/input/irpMerged'
-- ***************************************************************************

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


-- create irp merged events table 
DROP TABLE IF EXISTS irpMerged;
CREATE EXTERNAL TABLE irpMerged (
  term INT,
  crn INT,
  section STRING,
  credits FLOAT,
  time STRING,
  gpa FLOAT,
  enrollment INT,
  difficulty INT,
  department STRING,
  fname STRING,
  lname STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/input/irpMerged';



INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_class'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT course_num, avg(gpa), min(gpa), max(gpa), avg(enrollment), min(enrollment), max(enrollment)
FROM irp
GROUP BY course_num;


INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_dept'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT department, avg(gpa), min(gpa), max(gpa)
FROM irpMerged
GROUP BY irpMerged.department;


INSERT OVERWRITE LOCAL DIRECTORY 'stats_per_term'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT term, avg(gpa), min(gpa), max(gpa), avg(enrollment), min(enrollment), max(enrollment)
FROM irp
GROUP BY irp.term;
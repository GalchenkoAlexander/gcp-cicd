CREATE EXTERNAL TABLE IF NOT EXISTS movies_text (
  movieId           int,
  title             string,
  genres            string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'gs://gcp-cicd-artifacts/hive/input'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS movies (
  movieId           int,
  title             string,
  genres            string
)
STORED AS ORC
LOCATION 'gs://gcp-cicd-artifacts/hive/output';

INSERT OVERWRITE TABLE movies
select movieId, title, genres from movies_text;

DROP TABLE IF EXISTS movies_text;

ANALYZE TABLE movies COMPUTE STATISTICS;
CREATE EXTERNAL TABLE IF NOT EXISTS movies_text (
  movieId           int,
  title             string,
  genres            string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'gs://${PROJECT_ID}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA}/hive/input'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE IF NOT EXISTS movies
STORED AS ORC
LOCATION 'gs://${PROJECT_ID}/${REPO_NAME}/${BRANCH_NAME}/${SHORT_SHA}/hive/output/'
as
select 'movies_text' as movies, count(*) as cnt from movies_text

DROP TABLE IF EXISTS movies_text;

ANALYZE TABLE movies COMPUTE STATISTICS;
# nanodegree-log-analysis
This project goal is to analyse stored in database logs and answer 3 questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Dependencies.
To install psycopg2 run (make sure you have pip installed):
pip3 install psycopg2
Follow the link:
filehttps://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
to download sql file and unzip it to project directory

run 'psql -d news -f newsdata.sql'
run 'psql -d news -f views.sql'
run 'python3 log_parser.py'

The answer will be printed to the console
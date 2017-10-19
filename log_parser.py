# -*- coding: utf-8 -*-
import psycopg2


def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        database = psycopg2.connect("dbname={}".format(database_name))
        cursor = database.cursor()
        return database, cursor
    except psycopg2.Error as exception:
        raise exception


def create_view(query, connection, cursor):
    cursor.execute(query)
    connection.commit()


def get_answer(cursor, query, template):
    cursor.execute(query)
    for line in cursor.fetchall():
        print(template % line)


if __name__ == '__main__':
    try:
        connection, cursor = connect('news')
    except:
        print('Unable to connect to database')
    else:
        create_view(
            '''
                create or replace view article_views as
                select r.title
                ,a.name
                ,count(l.path) as count_views from log l
                inner join articles r on l.path = '/article/' || r.slug
                inner join authors a on a.id = r.author
                where l.path != '/'
                group by r.title, a.name
                order by count_views desc
                ''',
            connection,
            cursor
        )
        print('1. What are the most popular three articles of all time?')
        get_answer(
            cursor,
            '''
              select title, count_views from article_views
              limit 3;
              ''',
            '%s — %s views'
        )

        print('2. Who are the most popular article authors of all time?')
        get_answer(
            cursor,
            '''
              select name, sum(count_views) as author_views from article_views
              group by name
              order by author_views desc;
            ''',
            '%s — %s views'
        )

        print('3. On which days did more than 1% of requests lead to errors?')
        create_view(
            '''
                create or replace view requests as
                select 
                time::date as day
                ,count(status) as views
                from log
                group by day
                ''',
            connection,
            cursor
        )
        create_view(
            '''
                create or replace view fails as
                select 
                time::date as day
                ,count(status) as views
                from log
                where status != '200 OK'
                group by day
                ''',
            connection,
            cursor
        )
        get_answer(
            cursor,
            '''
                select to_char(r.day, 'Month DD, YYYY')
                ,round((f.views * 100)::numeric/r.views, 2) as percentage from requests r
                inner join fails f on f.day = r.day
                where (f.views * 100)::numeric/r.views > 1
                ''',
            '%s — %s%% errors'
        )

        cursor.close()
        connection.close()

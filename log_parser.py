import psycopg2

connection = psycopg2.connect('dbname=news')
cursor = connection.cursor()


if __name__ == '__main__':
    cursor.execute('''
        create or replace view article_views as
        select r.title
        ,a.name
        ,count(l.path) as count_views from log l
        inner join articles r on l.path = '/article/' || r.slug
        inner join authors a on a.id = r.author
        where l.path != '/'
        group by r.title, a.name
        order by count_views desc
    ''')
    connection.commit()
    print('1. What are the most popular three articles of all time?')
    cursor.execute('''
        select title, count_views from article_views
        limit 3;
    ''')
    popular_articles = cursor.fetchall()
    for article in popular_articles:
        print('%s — %s views' % (article[0], article[1]))

    print('2. Who are the most popular article authors of all time?')
    cursor.execute('''
        select name, sum(count_views) as author_views from article_views
        group by name
        order by author_views desc;
    ''')
    popular_authors = cursor.fetchall()
    for author in popular_authors:
        print('%s — %s views' % (author[0], author[1]))
    print('3. On which days did more than 1% of requests lead to errors?')
    cursor.execute('''
        create or replace view requests as
        select 
        time::date as day
        ,count(status) as views
        from log
        group by day
    ''')
    connection.commit()
    cursor.execute('''
        create or replace view fails as
        select 
        time::date as day
        ,count(status) as views
        from log
        where status != '200 OK'
        group by day
    ''')
    connection.commit()
    cursor.execute('''
        select to_char(r.day, 'Month DD, YYYY')
        ,round((f.views * 100)::numeric/r.views, 2) as percentage from requests r
        inner join fails f on f.day = r.day
        where (f.views * 100)::numeric/r.views > 1
        limit 10;
    ''')
    fail_days = cursor.fetchall()
    for day in fail_days:
        print('%s — %s%% errors' % (day[0], day[1]))
    cursor.close()
    connection.close()

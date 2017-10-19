create or replace view article_views as
  select
    r.title
    ,a.name
    ,count(l.path) as count_views from log l
  inner join articles r on l.path = '/article/' || r.slug
  inner join authors a on a.id = r.author
  where l.path != '/'
  group by r.title, a.name
  order by count_views desc;


create or replace view requests as
  select
    time::date as day
    ,count(status) as views
  from log
  group by day;


create or replace view fails as
  select
    time::date as day
    ,count(status) as views
  from log
  where status != '200 OK'
  group by day;

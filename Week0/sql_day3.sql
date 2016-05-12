

Goals
Explore the Database
Basic Querying - Selecting From Tables
Selecting specific attributes of a table
Where clause/ filtering
Aggregation functions: counting
Aggregation functions: AVG
Intervals, Ranges, and sorting
Subqueries
Loading the database


In this repo, there's a SQL dump of the data we'll be using today.

If you are on your personal computer and havent set up postgres yet, follow these instructions

From the command line run psql and then this command to create the database.

CREATE DATABASE readychef;
\q
Navigate to where you cloned this very repository and run the following commands to import the database:

cd data
psql readychef < readychef.sql
You should see a bunch of SQL commands flow through the terminal.

To enter the interactive Postgres prompt, now enter the following to be connected or your database.

psql readychef
Now we are in a command line client. This is how we will explore the database to gain an understanding of what data we are playing with.

Basic Exploration
First, we will want to see what the available tables are. Remember, now that we are in the database, all of our commands or actions will be on the readychef database.

What are the tables in our database? Run \d to find out.

What columns does each table have? Run \d tablename to find out.

Select statements
To get an understanding of the data, run a SELECT statement on each table. Keep all the columns and limit the number of rows to 10.  SELECT * FROM EVENTS LIMIT 10;

SELECT *
FROM users
LIMIT 10;

SELECT *
FROM events
LIMIT 10;

SELECT *
FROM meals
LIMIT 10;

SELECT *
FROM referrals
LIMIT 10;

SELECT *
FROM visits
LIMIT 10;




Write a SELECT statement that would get just the userids.

SELECT userid
FROM visits
LIMIT 10;


Maybe youre just interested in what the campaign ids are. Use 'SELECT DISTINCT' to figure out all the possible values of that column.

SELECT DISTINCT campaign_id
FROM users;


Note: Pinterest=PI, Facebook=FB, Twitter=TW, and Reddit=RE




Where Clauses / Filtering
Now that we have the lay of the land, we are interested in the subset of users that came from Facebook (FB). If youre unfamiliar with SQL syntax, the WHERE clause can be used to add a conditional to SELECT statements. This has the effect of only returning rows where the conditional evaluates to TRUE.

Note: Make sure you put string literals in single quotes, like campaign_id='TW'.

Using the WHERE clause, write a new SELECT statement that returns all rows where Campaign_ID is equal to FB.



SELECT userid, dt FROM users
WHERE campaign_id='FB';



We dont need the campaign id in the result since they are all the same, so only include the other two columns.

Your output should be something like this:

 userid |     dt
--------+------------
      3 | 2013-01-01
      4 | 2013-01-01
      5 | 2013-01-01
      6 | 2013-01-01
      8 | 2013-01-01
...
Aggregation Functions
Lets try some aggregation functions now.

COUNT is an example aggregate function, which counts all the entries and you can use like this:

SELECT COUNT(*) FROM users;
Your output should look something like:

 count
-------
  5524
(1 row)

Write a query to get the count of just the users who came from Facebook.

SELECT COUNT(userid) FROM users
WHERE campaign_id = 'FB';




Now, count the number of users coming from each service. Here youll have to group by the column youre selecting with a GROUP BY clause.

SELECT campaign_id, COUNT(userid) FROM users
GROUP BY campaign_id;


Try running the query without a group by. Postgres will tell you what to put in your group by clause!

Use COUNT (DISTINCT columnname) to get the number of unique dates that appear in the users table.


SELECT COUNT(DISTINCT dt) FROM users;




Theres also MAX and MIN functions, which do what you might expect. Write a query to get the first and last registration date from the users table.

SELECT MAX(dt) FROM users;
SELECT MIN(dt) FROM users;



Calculate the mean price for a meal (from the meals table). You can use the AVG function. Your result should look like this:

         avg
---------------------
 10.6522829904666332
(1 row)


SELECT AVG(price) FROM meals;





Now get the average price, the min price and the max price for each meal type. Dont forget the group by statement!


SELECT type, AVG(price), MIN(price), MAX(price) FROM meals
GROUP BY type;




Your output should look like this:

    type    |         avg         | min | max
------------+---------------------+-----+-----
 mexican    |  9.6975945017182131 |   6 |  13
 french     | 11.5420000000000000 |   7 |  16
 japanese   |  9.3804878048780488 |   6 |  13
 italian    | 11.2926136363636364 |   7 |  16
 chinese    |  9.5187165775401070 |   6 |  13
 vietnamese |  9.2830188679245283 |   6 |  13
(6 rows)

Its often helpful for us to give our own names to columns. We can always rename columns that we select by doing AVG(price) AS avg_price. This is called aliasing. Alias all the above columns so that your table looks like this:

    type    |      avg_price      | min_price | max_price
------------+---------------------+-----------+-----------
 mexican    |  9.6975945017182131 |         6 |        13
...



SELECT type, AVG(price) as avg_price, MIN(price) as min_price, MAX(price) as max_price
FROM meals
GROUP BY type;







Maybe you only want to consider the meals which occur in the first quarter (January through March). Use date_part to get the month like this: date_part('month', dt). Add a WHERE clause to the above query to consider only meals in the first quarter of 2013 (month<=3 and year=2013).


SELECT date_part('month', dt) as month, AVG(price) as avg_price,
        MIN(price) as min_price, MAX(price) as max_price
FROM meals
WHERE date_part('month', dt) <=3 and date_part('year', dt)=2013
GROUP BY dt;


There are also scenarios where you'd want to group by two columns. Modify the above query so that we get the aggregate values for each month and type. You'll need to add the month to both the select statement and the group by statement.


SELECT type, date_part('month', dt) as month, AVG(price) as avg_price,
        MIN(price) as min_price, MAX(price) as max_price
FROM meals
WHERE date_part('month', dt) <=3 and date_part('year', dt)=2013
GROUP BY type, date_part('month', dt);


It'll be helpful to alias the month column and give it a name like month so you don't have to call the date_time function again in the GROUP BY clause.

Your result should look like this:

    type    | month |      avg_price      | min_price | max_price
------------+-------+---------------------+-----------+-----------
 italian    |     2 | 11.2666666666666667 |         7 |        16
 chinese    |     1 | 11.2307692307692308 |         8 |        13
...
From the events table, write a query that gets the total number of buys,
likes and shares for each meal id. Extra: To avoid having to do this as
three separate queries you can do the count of the number of buys
like this: SUM(CASE WHEN event='bought' THEN 1 ELSE 0 END).



SELECT SUM(CASE WHEN event='bought' THEN 1 ELSE 0 END) as bought,
       SUM(CASE WHEN event='like'   THEN 1 ELSE 0 END) as likes,
       SUM(CASE WHEN event='share'  THEN 1 ELSE 0 END) as share
FROM events;






Sorting
Lets start with a query which gets the average price for each type. It
will be helpful to alias the average price column as 'avg_price'.


SELECT type, AVG(price) as avg_price
FROM meals
GROUP BY type;




To make it easier to read, sort the results by the type column. You can
do this with an ORDER BY clause.

Now return the same table again, except this time order by the price in
descending order (add the DESC keyword).

SELECT type, AVG(price) as avg_price
FROM meals
GROUP BY type
ORDER BY avg_price DESC;





Sometimes we want to sort by two columns. Write a query to get all the
meals, but sort by the type and then by the price. You should have an
order by clause that looks something like this: ORDER BY col1, col2.




SELECT type, AVG(price) as avg_price
FROM meals
GROUP BY type
ORDER BY type, avg_price DESC;



For shorthand, people sometimes use numbers to refer to the columns in
their order by or group by clauses. The numbers refer to the order they
are in the select statement. For instance SELECT type, dt FROM meals
ORDER BY 1; would order the results by the type column.


SELECT type, AVG(price) as avg_price
FROM meals
GROUP BY type
ORDER BY 1, 2 DESC;






Joins
Now we are ready to do operations on multiple tables. A JOIN allows us
to combine multiple tables.

Write a query to get one table that joins the events table with the
users table (on userid) to create the following table.

 userid | campaign_id | meal_id | event
--------+-------------+---------+--------
      3 | FB          |      18 | bought
      7 | PI          |       1 | like
     10 | TW          |      29 | bought
     11 | RE          |      19 | share
     15 | RE          |      33 | like
...


SELECT users.userid, campaign_id, meal_id, event FROM events
JOIN users
  ON users.userid = events.userid;





Also include information about the meal, like the type and the price.
Only include the bought events. The result should look like this:

 userid | campaign_id | meal_id |    type    | price
--------+-------------+---------+------------+-------
      3 | FB          |      18 | french     |     9
     10 | TW          |      29 | italian    |    15
     18 | TW          |      40 | japanese   |    13
     22 | RE          |      23 | mexican    |    12
     25 | FB          |       8 | french     |    14
...


SELECT users.userid, campaign_id, events.meal_id, type, price FROM events
JOIN users
  ON users.userid = events.userid and event = 'bought'
JOIN meals
  ON events.meal_id = meals.meal_id;





If your results are different, make sure you filtered it so you only got
the bought events. You should be able to do this without using a where
clause, only on clause(s)!

Write a query to get how many of each type of meal were bought.

You should again be able to do this without a where clause!


SELECT type, COUNT(type) FROM events
JOIN users
  ON users.userid = events.userid and event='bought'
JOIN meals
  ON events.meal_id = meals.meal_id
GROUP BY type;






Phew! If you've made it this far, congratulations! You're ready to
move on to subqueries.

Extra Credit (pt. 1)
Subqueries
In a subquery, you have a select statement embedded in another select
statement.

Write a query to get meals that are above the average meal price.

Start by writing a query to get the average meal price. Then write a
query where you put price > (SELECT ...) (that select statement should
  return the average price).

SELECT type, price>(SELECT AVG(price) FROM meals) FROM meals
GROUP BY type;



Write a query to get the meals that are above the average meal price for
that type.

Here youll need to use a join. First write a query that gets the average
meal price for each type. Then join with that table to get ones that are
larger than the average price for that meal. Your query should look
something like this:

SELECT meals.*
FROM meals
JOIN (SELECT ...) average
ON ...
Note that you need to fill in the select statement that will get the
average meal price for each type. We alias this table and give it the
name average (you can include the AS keyword, but it doesnt matter).

Modify the above query to give a count of the number of meals per type
that are above the average price.

Calculate the percentage of users which come from each service. This
query will look similar to #2 from aggregation functions, except you
have to divide by the total number of users.

Like with many programming languages, dividing an int by an int yields
an int, and you will get 0 instead of something like 0.54. You can deal
with this by casting one of the values as a real like this: CAST
(value AS REAL)

You should get a result like this:

 campaign_id |      percent
-------------+-------------------
 RE          | 0.156046343229544
 FB          | 0.396813902968863
 TW          | 0.340695148443157
 PI          | 0.106444605358436
(4 rows)





Extra Credit (pt. 2)
Answer the question, "What user from each campaign bought the most items?"

It will be helpful to create a temporary table that contains
the counts of the number of items each user bought. You can
create a table like this: CREATE TABLE mytable AS SELECT...

For each day, get the total number of users who have registered
as of that day. You should get a table that has a dt and a cnt column.
This is a cumulative sum.

What day of the week gets meals with the most buys?

Which month had the highest percent of users who visited the site
purchase a meal?

Find all the meals that are above the average price of the previous 7 days.

What percent of users have shared more meals than they have liked?

For every day, count the number of users who have visited the site
and done no action.

Find all the dates with a greater than average number of meals.

Find all the users who bought a meal before liking or sharing a meal.

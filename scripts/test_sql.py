"""Test that SQL queries work properly"""

import sqlite3

QUERY1 = """
        SELECT date, approval
        FROM biden_approval
        WHERE SUBSTR(date, 6, 2) IN ('09', '10', '11')
        AND SUBSTR(date, 1, 4) = '2022'
        ORDER BY approval DESC
        LIMIT 10
        """

QUERY2 = """
        SELECT date, sum(retweet_count) as retweets
        FROM
            (SELECT id, name, SUBSTR(created_at, 1, 10) as date,
            favorite_count, retweet_count, text
            FROM biden_tweets)
        GROUP BY date
        ORDER BY retweets DESC
        LIMIT 10
        """

QUERY3 = """
        SELECT AVG(approval) as mean_approval
        FROM biden_approval
        """

QUERY4 = """
        WITH tweets(date, favorites, retweet_count) AS
        (SELECT date, sum(favorite_count) as favorites, sum(retweet_count) as retweets
             FROM
            (SELECT id, name, SUBSTR(created_at, 1, 10) as date,
            favorite_count, retweet_count, text
             FROM biden_tweets)
             GROUP BY date)
        SELECT AVG(retweet_count)
        FROM tweets
        """

QUERY5 = """
        WITH tweets(date, favorites, retweet_count) AS
        (SELECT date, sum(favorite_count) as favorites, sum(retweet_count) as retweets
             FROM
            (SELECT id, name, SUBSTR(created_at, 1, 10) as date,
            favorite_count, retweet_count, text
             FROM biden_tweets)
             GROUP BY date)
        SELECT t.date, t.retweet_count, a.approval
        FROM tweets t
        INNER JOIN biden_approval a
        ON t.date = a.date
        ORDER BY a.approval DESC
        LIMIT 10
        """

# Initiate a connection and a cursor for the database
conn = sqlite3.connect("data/biden_tweets.db")
cursor = conn.cursor()

# Test that the first query returns 10 results
assert len(cursor.execute(QUERY1).fetchall()) == 10

# Test that the second query returns 10 results
assert len(cursor.execute(QUERY2).fetchall()) == 10

# Test that the mean approval rating is in between 0 and 100
assert (cursor.execute(QUERY3).fetchone()[0] > 0) & (
    cursor.execute(QUERY3).fetchone()[0] < 100
)

# Test that the mean retweet number is greater than 0
assert cursor.execute(QUERY4).fetchone()[0] > 0

# Test that the merged query returns 10 results
assert len(cursor.execute(QUERY5).fetchall()) == 10

conn.close()

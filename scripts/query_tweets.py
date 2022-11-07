import sqlite3

# Initiate a connection and a cursor for the database
conn = sqlite3.connect("data/biden_tweets.db")
cursor = conn.cursor()

# Our first question: what dates were Biden's approval rating the highest
QUERY1 = """
        SELECT date, approval
        FROM biden_approval
        WHERE SUBSTR(date, 6, 2) IN ('09', '10', '11')
        AND SUBSTR(date, 1, 4) = '2022'
        ORDER BY approval DESC
        LIMIT 10
        """

best_approvals = cursor.execute(QUERY1).fetchall()
print("Joe Biden's approval ratings were highest on these dates.")
for i in range(10):
    print(
        f"Biden had a approval rating of {best_approvals[i][1]:.2f}% on {best_approvals[i][0]}."
    )
print()

# Our second question: on what dates did Biden get the most retweets?
# (Note: our twitter data only goes as far back as Sept. 2022)

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

most_retweets = cursor.execute(QUERY2).fetchall()
print("Joe Biden's twitter retweets were highest on these dates.")
for i in range(10):
    print(f"Biden had {most_retweets[i][1]} retweets on {most_retweets[i][0]}.")
print()

# Our third question: what is the mean approval rating for Biden
QUERY3 = """
        SELECT AVG(approval) as mean_approval
        FROM biden_approval
        """
mean_approval = cursor.execute(QUERY3).fetchone()
print(
    f"""Joe Biden's mean approval rating, as published by the FiveThirtyEight aggregate poll is {mean_approval[0]:.2f}%."""
)
print()


# Our fourth question: what is the mean retweet count for Biden?
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
mean_retweets = cursor.execute(QUERY4).fetchone()
print(f"Joe Biden's tweets get retweeted by {mean_retweets[0]} users daily on average.")
print()

# Our final question:
# Are higher approval ratings usually associated with higher retweet counts for Biden's twitter

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

first_five_results = cursor.execute(QUERY5).fetchall()
for i in range(10):
    print(
        f"""On {first_five_results[i][0]}, 
        Biden had {first_five_results[i][1]} retweets,
         and an approval rating of {first_five_results[i][2]:.2f}%."""
    )
conn.close()

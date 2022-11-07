import csv
import sqlite3

# Connect to the biden_tweets.db database
conn = sqlite3.connect(database="data/biden_tweets.db")

# Create cursor, with which we can execute SQL commands
cursor = conn.cursor()

# Create a table for all the tweets
cursor.execute(
    """
    CREATE TABLE biden_tweets(
        id INTEGER,
        name TEXT,
        created_at TEXT,
        favorite_count INTEGER,
        retweet_count INTEGER,
        text TEXT
    )
    """
)

# Create another table for biden's daily approval rating
cursor.execute(
    """
    CREATE TABLE biden_approval(
        approval REAL,
        disapproval REAL,
        date TEXT
    )
    """
)

# Create a SQL command that inserts records from the csv into the table
TWEETS = "INSERT INTO biden_tweets (id, name, created_at, favorite_count, retweet_count, text) VALUES(?, ?, ?, ?, ?, ?)"
APPROVAL = "INSERT INTO biden_approval (approval, disapproval, date) VALUES(?, ?, ?)"

# Open the tweets data
file_tweets = open("data/@JoeBiden_tweets.csv", mode="r", encoding="utf-8")
file_approval = open("data/approval.csv", mode="r", encoding="utf-8")

# Read the csv file
contents_tweets = csv.reader(file_tweets)
contents_approval = csv.reader(file_approval)
# Skip over first row
next(contents_tweets, None)
next(contents_approval, None)

# Insert the tweets into the biden_tweets table
cursor.executemany(TWEETS, contents_tweets)
cursor.executemany(APPROVAL, contents_approval)

conn.commit()
conn.close()

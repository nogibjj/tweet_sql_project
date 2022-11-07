# tweet_sql_project
This project aims to use twitter data to understand whether President Joe Biden's approval rating has anything to do with how many retweets he gets on twitter in a given day. I used Tweepy to collect the data from Twitter and SQLite to construct and populate a database, where I conduct further data analysis. 

Here is a project schema:
![project3_schema](https://user-images.githubusercontent.com/60377132/200221799-6ec9b3b5-2991-46aa-a913-5504747e5b60.png)

## Bash CLI tool to scrape and transform Twitter Data

For the first part of this project, I built a Click command line tool to scrape Twitter data by giving it a user name. 
For textual analysis and sentiment analysis, Twitter data is fundamental in important ways. 

### Twitter Authentication and Data Scraping

I used GitHub Code Space's builtin secrets option to add my Twitter API key, secret, access token, and access token secret. The extract.py script is a Click application that authenticates to Twitter using these API authentifications and retrieves the most recent tweets from the handle that is inputed by the user. 

### Constructing SQLite Database

In the tweet_to_sql.py script, I created a database called biden_tweets.db and established a connection to it in SQLite. I created two tables, one for the tweet data collected from the Tweepy API and another for Biden's approval rating, which is sourced from FiveThirtyEight's aggregated tracker.
I specified the fields required to create the tables and populated them with the csvs from the data folder.
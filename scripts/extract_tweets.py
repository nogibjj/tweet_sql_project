import click
import tweepy
import pandas as pd
import os

# Authenticate to twitter, make sure you have a config.ini file in your repository
def get_access():
    """Authenticate to twitter"""
    # Authentication Details
    api_key = os.environ["TWITTER_API_KEY"]
    api_key_secret = os.environ["TWITTER_API_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SCECRET"]
    # Authenticate
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)  # We use this to get access to our twitter account
    return api


@click.command()
@click.option(
    "--name",
    "-n",
    default=["@JoeBiden", "@SpeakerPelosi", "@SenSchumer"],
    help="Twitter handle to collect tweets from",
    multiple=True,
)
@click.option("--count", "-c", default=200, help="Number of tweets to collect")
def get_tweets(name, count):
    """Retrieve tweet information from the API object"""
    api = get_access()
    for handle in name:
        tweets_all = api.user_timeline(
            screen_name=handle, count=count, include_rts=False, tweet_mode="extended"
        )

        outtweets = [
            [
                tweet.id,
                tweet.user.screen_name,
                tweet.created_at,
                tweet.favorite_count,
                tweet.retweet_count,
                tweet.full_text.encode("utf-8").decode("utf-8"),
            ]
            for tweet in tweets_all
        ]

        df = pd.DataFrame(
            outtweets,
            columns=[
                "id",
                "name",
                "created_at",
                "favorite_count",
                "retweet_count",
                "text",
            ],
        )
        df.to_csv("data/%s_tweets.csv" % handle, index=False)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    get_tweets()

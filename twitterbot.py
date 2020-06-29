import tweepy
import logging
from twitterconfig import create_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                screenname = tweet.user.screen_name
                idn = tweet.id
                url = f'https://twitter.com/{screenname}/status/{idn}'
                stat = "ENTER TEXT HERE #ENTERHASHTAGTOTRENDHERE "+url
                self.api.update_status(stat)
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    
    def on_error(self, status, status_code):
        logger.error(status)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["#"])   #separate with commas if your streamer is listening to multiple hashtags
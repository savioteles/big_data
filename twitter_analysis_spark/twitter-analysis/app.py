import json
from kafka import SimpleProducer, KafkaClient
import tweepy
import configparser

class TweeterStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        client = KafkaClient("10.0.2.15:9092")
        self.producer = SimpleProducer(client, async = True,
                          batch_send_every_n = 1000,
                          batch_send_every_t = 10)

    def on_status(self, status):
        msg =  status.text.encode('utf-8')
        try:
            self.producer.send_messages(b'twitterstream', msg)
        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status_code):
        print("Error received in kafka producer")
        return True 

    def on_timeout(self):
        return True 

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('twitter-app-credentials.txt')
    consumer_key = config['DEFAULT']['consumerKey']
    consumer_secret = config['DEFAULT']['consumerSecret']
    access_key = config['DEFAULT']['accessToken']
    access_secret = config['DEFAULT']['accessTokenSecret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    while True:
        try:
            # Connect/reconnect the stream
            stream = tweepy.Stream(auth, listener = TweeterStreamListener(api))
            stream.filter(locations=[-180,-90,180,90], languages = ['en'], stall_warnings=True)
        except IncompleteRead:
            # Reconnect
            continue
        except KeyboardInterrupt:
            # Exit this loop
            stream.disconnect()
            break

    

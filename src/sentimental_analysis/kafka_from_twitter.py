import os
import re
import json
import tweepy
import threading
import configparser
from kafka import SimpleProducer, KafkaClient

access_token = "xxxx"
access_token_secret = "xxxx"
consumer_key = "xxxx"
consumer_secret = "xxxx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class TweeterStreamListener(tweepy.StreamListener):
    """ A class to read the twitter stream and push it to Kafka"""

    def __init__(self, api, topic_name):
        self.api = api
        self.topic_name = topic_name
        super(tweepy.StreamListener, self).__init__()
        client = KafkaClient("localhost:9092")
        self.producer = SimpleProducer(client, async=True,
                                       batch_send_every_n=1000,
                                       batch_send_every_t=10)

    def on_status(self, status):
        """ This method is called whenever new data arrives from live stream.
        We asynchronously push this data to kafka queue"""
        msg = status.text.encode('utf-8')
        try:
            self.producer.send_messages(self.topic_name, msg)
            print(self.topic_name)
            print(msg)
        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status_code):
        print("Error received in kafka producer")
        return True

    def on_timeout(self):
        return True


class Producer:
    """docstring for Producer."""

    def __init__(self, topic_name):
        self.topic_name = topic_name
        self.api = tweepy.API(auth)
        self.stream = tweepy.Stream(auth,
                                    listener=TweeterStreamListener(self.api,
                                                                   topic_name))

    def run_producer(self):
        self.stream.filter(track=[self.topic_name], languages=['en'])


if __name__ == '__main__':
    topics = ["spiderman", "avengers", "superman"]
    #topics = ["spiderman"]
    producer = [None] * len(topics)
    thread_producer = [None] * len(topics)
    for iterator in range(len(topics)):
        producer[iterator] = Producer(topics[iterator])
        thread_producer[iterator] = threading.Thread(target=producer[iterator].run_producer,
                                                     args=())
        thread_producer[iterator].start()

    for iterator in range(len(topics)):
        thread_producer[iterator].join()

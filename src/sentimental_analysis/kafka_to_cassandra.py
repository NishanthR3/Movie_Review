import re
import threading
from kafka import KafkaConsumer

# To consume messages


class Consumer(object):
    """docstring for Consumer."""

    def __init__(self, topic_name):
        self.topic_name = topic_name
        self.consumer = KafkaConsumer(topic_name,
                                      group_id=None,
                                      bootstrap_servers=['localhost:9092'],
                                      api_version=(0, 10))

    @staticmethod
    def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def show_messages(self):
        for message in self.consumer:
            print(self.topic_name)
            print(self.clean_tweet(message.value.decode('utf-8')))


if __name__ == '__main__':
    topics = ["spiderman", "avengers", "superman"]
    #topics = ["spiderman"]
    consumer = [None] * len(topics)
    thread_consumer = [None] * len(topics)
    for iterator in range(len(topics)):
        consumer[iterator] = Consumer(topics[iterator])
        thread_consumer[iterator] = threading.Thread(target=consumer[iterator].show_messages,
                                                     args=())
        thread_consumer[iterator].start()

    for iterator in range(len(topics)):
        thread_consumer[iterator].join()

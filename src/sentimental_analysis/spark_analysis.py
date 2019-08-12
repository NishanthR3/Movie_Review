import re
import sys
import threading
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from textblob import TextBlob
from update_movie_review import Movie

movie = Movie()


def spark_analysis(topic_name):
    sc = SparkContext(appName="PythhonSpark")
    ssc = StreamingContext(sc, 60)
    kvs = KafkaUtils.createDirectStream(
        ssc, [topic_name], {"metadata.broker.list": "localhost:9092"})

    lines = kvs.map(lambda x: x[1].encode("ascii", "ignore"))
    words = lines.flatMap(lambda line: line.split("\n"))
    review = words.map(lambda word: (topic_name,
                                     [analyze_sentiment(topic_name, word), 1]))
    answer = review.reduceByKey(lambda x, y: [x[0] + y[0], x[1] + y[1]])

    answer.pprint()
    ssc.start()
    #ssc.awaitTermination()
    ssc.awaitTerminationOrTimeout(600)


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analyze_sentiment(topic_name, tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        movie.update_review(topic_name, 3, 1)
        return 1
    elif analysis.sentiment.polarity < 0:
        movie.update_review(topic_name, 1, 1)
        return -1
    else:
        movie.update_review(topic_name, 2, 1)
        return 0


if __name__ == "__main__":
    topic_name = sys.argv[2]
    spark_analysis(topic_name)

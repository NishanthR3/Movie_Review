#!/bin/bash
#topics=("spiderman" "avengers" "superman")
topics=("avengers")
for iterator in "${topics[@]}"
do
  #echo $iterator
  #spark-2.3.2-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 spark_analysis.py $iterator &
  ./bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 ../spark_analysis.py localhost:9092 $iterator &
  #./bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 ../spark_analysis.py localhost:9092 $iterator
  sleep 60
done

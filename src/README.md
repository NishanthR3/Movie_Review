# Flask Web App

## Running the flask server

1. Go to **src/app** directory.
2. Install all the python3 dependencies using the **pip3** package manager.
3. Run the following command:
```
$ python3 app.py
```
<br/>

# Sentimental Analysis on Twitter Data

## Getting twitter data and storing it

1. Go to **src/sentimental_analysis** directory.
2. Start Kafka servers by running following commands in **different terminals** after going into **kafka_2.11-2.0.0** directory:
```
$ bin/zookeeper-server-start.sh config/zookeeper.properties
$ bin/kafka-server-start.sh config/server.properties
```
3. Install all the python3 dependencies using **pip3** package manager.
4. For getting twitter data, run the following command:
```
$ python3 kafka_from_twitter.py
```
5. For storing this data, go to a **different terminal** and run the Kafka consumer with the following command:
```
$ python3 kafka_to_cassandra.py
```

## Spark server for sentimental Analysis

1. Go to **src/sentimental_analysis** directory.
2. For running one script on Spark server with the script for sentimental analysis, run the following command:
```
$ spark-2.3.2-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 spark_analysis.py
```
3. For running many scripts on Spark server with script for sentimental analysis, run the following commands:
```
$ chmod 777 spark_run.sh
$ ./spark_run.sh
```

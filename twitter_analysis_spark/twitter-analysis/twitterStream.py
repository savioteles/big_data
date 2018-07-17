import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka_2.10:1.5.1 pyspark-shell'
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator

def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)

    ssc = StreamingContext(sc, 10)
    ssc.checkpoint("checkpoint")
    pwords = load_wordlist("./Dataset/positive.txt")
    nwords = load_wordlist("./Dataset/negative.txt")
    counts = stream(ssc, pwords, nwords, 100)
    print "\n\nAnalise de sentimento no Twitter ao longo do tempo:\n"
    print counts
    print "\n\n"

	
def load_wordlist(filename):
    words = {}
    f = open(filename, 'rU')
    text = f.read()
    text = text.split('\n')
    for line in text:
        words[line] = 1
    f.close()
    return words


def wordSentiment(word,pwords,nwords):
    if word in pwords:
	return ('positive', 1)
    elif word in nwords:
	return ('negative', 1)


def updateFunction(newValues, runningCount):
    if runningCount is None:
       runningCount = 0
    return sum(newValues, runningCount) 


def sendRecord(record):
    connection = createNewConnection()
    connection.send(record)
    connection.close()


def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(
    ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1].encode("ascii", "ignore"))

    words = tweets.flatMap(lambda line:line.split(" "))
    positive = words.map(lambda word: ('Positive', 1) if word in pwords else ('Positive', 0))
    negative = words.map(lambda word: ('Negative', 1) if word in nwords else ('Negative', 0))
    allSentiments = positive.union(negative)
    sentimentCounts = allSentiments.reduceByKey(lambda x,y: x+y)
    runningSentimentCounts = sentimentCounts.updateStateByKey(updateFunction)
    runningSentimentCounts.pprint()
    
    counts = []
    sentimentCounts.foreachRDD(lambda t, rdd: counts.append(rdd.collect()))
    
    ssc.start() 
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully = True)

    return counts


if __name__=="__main__":
    main()

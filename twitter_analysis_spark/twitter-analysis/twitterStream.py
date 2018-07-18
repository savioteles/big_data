# -*- coding: utf-8 -*-
# Importa a biblioteca do spark-kafka
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka_2.10:1.5.1 pyspark-shell'
# Bibliotecas do Spark Streaming
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
# Biblioteca do Kafka
from pyspark.streaming.kafka import KafkaUtils

def main():
	# Configura o Spark para rodar localmente com o nome 'Streamer' da aplicação
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    # Como o Spark roda em micro batchs, configura o batch em intervalos de 10 segundos
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint("checkpoint")

    # Carrega as palavras positivas do arquivo positive.txt
    pwords = load_wordlist("./Dataset/positive.txt")
    # Carrega as palavras negativas do arquivo negative.txt
    nwords = load_wordlist("./Dataset/negative.txt")
    # Chama o método stream local passando o contexto do Spark, os vetores com palavras positivas e negativas e a duração do stream de 30 segundos
    counts,all_counts = stream(ssc, pwords, nwords, 30)
    print "\n\nAnalise de sentimento no Twitter ao longo do tempo:\n"
    print "Número total de tweets negativos e positivos: \n"
    print all_counts[-1]
    print "\n\nNúmero de tweets positivos e negativos ao longo do tempo: \n"
    print counts
    print "\n\n"

# Esta função lê as palavras de cada linha de um arquivo e retorna em um vetor
def load_wordlist(filename):
    words = {}
    f = open(filename, 'rU')
    text = f.read()
    text = text.split('\n')
    for line in text:
        words[line] = 1
    f.close()
    return words

#Esta função é utilizada para somar o total de tweets com sentimento positivo e negativo que já chegaram
def updateFunction(newValues, runningCount):
    if runningCount is None:
       runningCount = 0
    return sum(newValues, runningCount) 

def stream(ssc, pwords, nwords, duration):
	# Cria um canal de comunicação com o servidor do Kafka que escuta o tópico twitterstream
    kstream = KafkaUtils.createDirectStream(
    ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})

    # Cria um stream lê as strings que chegam no tópico do Kafka
    tweets = kstream.map(lambda x: x[1].encode("ascii", "ignore"))
    # Para cada tweet que chega, faz um split por espaço para pegar as palavras
    words = tweets.flatMap(lambda line:line.split(" "))
    # Para cada palavra no tweet verifica se ela está na lista de positivas ou negativas.
    # Soma 1 se tiver na lista de palavras positivas
    positive = words.map(lambda word: ('Positive', 1) if word in pwords else ('Positive', 0))
    # Soma 1 se tiver na lista de palavras negativas
    negative = words.map(lambda word: ('Negative', 1) if word in nwords else ('Negative', 0))
    # Faz uma união dos vetores positivo e negativo
    allSentiments = positive.union(negative)
    # Faz uma agregação pela chave ('Positive' ou 'Negative') e soma os valores associados
    sentimentCounts = allSentiments.reduceByKey(lambda x,y: x+y)
    
    # Ao longo da execução do stream vai salvando e imprimindo na tela o estado do número total de tweets positivos e negativos que já chegaram
    runningSentimentCounts = sentimentCounts.updateStateByKey(updateFunction)
    runningSentimentCounts.pprint()
    all_counts = []
    runningSentimentCounts.foreachRDD(lambda t, rdd: all_counts.append(rdd.collect()))
    
    # Inicializa o vetor que irá guardar a análise de sentimento ao longo do tempo.
    counts = []
    # Cria o stream que irá rodar a análise de sentimento do Twitter ao longo do tempo
    sentimentCounts.foreachRDD(lambda t, rdd: counts.append(rdd.collect()))
    
    # Inicia o stream que irá executar por um intervalo de tempo (duration)
    ssc.start() 
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully = True)

    # Retorna o vetor com os resultados
    return counts,all_counts


if __name__=="__main__":
    main()

# -*- coding: utf-8 -*-
# Biblioteca cliente do Kafka
from kafka import SimpleProducer, KafkaClient
# Biblioteca para consumir os dados da API do Twitter
import tweepy
# Biblioteca para ler as configurações de chaves
import configparser

class TweeterStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        # Inicia o produtor que irá publicar os tweets no tópico do Kafka
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        client = KafkaClient("10.0.2.15:9092")
        self.producer = SimpleProducer(client, async = True,
                          batch_send_every_n = 1000,
                          batch_send_every_t = 10)

    def on_status(self, status):
        # Os tweets chegam nessa função a partir da API do Twitter
        msg =  status.text.encode('utf-8')
        try:
            # Envia os tweets para o tópico twitterstream do Kafka
            self.producer.send_messages(b'twitterstream', msg)
        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status_code):
        # Caso ocorra algum erro na coleta do Twitter
        print("Error received in kafka producer")
        return True 

    def on_timeout(self):
        return True 

if __name__ == '__main__':

    # Lê as chaves de acesso a API do Twitter que estão no arquivo twitter-app-credentials.txt
    config = configparser.ConfigParser()
    config.read('twitter-app-credentials.txt')
    consumer_key = config['DEFAULT']['consumerKey']
    consumer_secret = config['DEFAULT']['consumerSecret']
    access_key = config['DEFAULT']['accessToken']
    access_secret = config['DEFAULT']['accessTokenSecret']

    # Cria o cliente do Twitter passando as chaves de acesso
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    while True:
        try:
            # Conecta/reconecta no stream buscando os tweets com localização e em inglês
            stream = tweepy.Stream(auth, listener = TweeterStreamListener(api))
            stream.filter(locations=[-180,-90,180,90], languages = ['en'], stall_warnings=True)
        except KeyboardInterrupt:
            print "Bye!"
            # Se o usuário interromper a execução, termina o loop e disconecta da API do Twitter
            stream.disconnect()
            break
        except IncompleteRead:
            # Reconecta
            continue
        

    

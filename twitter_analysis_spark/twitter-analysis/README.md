#Twitter Sentiment Analytics com Apache Spark Streaming e Kafka

Nesse projeto iremos rodar um exemplo simples para uma análise de sentimentos do Twitter utilizando o Apache Spark e o Kafka. 

###Configuração do projeto
 
####Instalando as dependências
Para instalar todas as dependências, execute o script abaixo:

`$ sudo ./install.sh`
 
#### Inicializando o Kafka 

Nesta seção iremo iniciar a estrutura do kafka

##### Iniciar o zookeeper:  
`$ bin/zookeeper-server-start.sh config/zookeeper.properties`
 
##### Iniciar o servidor Kafka: 
`$ bin/kafka-server-start.sh config/server.properties`
 
##### Crie um tópico no Kafka: 
`$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitterstream`

##### Iniciar o consumidor para ler as mensagens do Kafka: 
`$ bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic twitterstream --from-beginning`
 
####Usando a API do Twitter
O script python app.py lê o stream de dados que chega do Twitter. Esse script irá precisar dos tokens de autenticação da sua conta no Twitter. 

Gere os tokens de acesso em: https://apps.twitter.com/

Atualize o arquivo `twitter-app-credentials.txt` com as chaves obtidas na api do Twitter.

Depois de atualizar o arquivo com as chaves do Twitter, você pode iniciar o download de tweets que serão escritos no tópico twitterstream do Kafka. 
Rode o seguinte comando:
`$ python app.py`   
Observação: Essa aplicação de coleta deve ficar rodando durante todo o tempo.
 

##### Executando a aplicação de análise com Spark
`$ $ sudo SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.1 twitterStream.py`

# Análise dos tweets utilizando Spark e Kafka

Neste tutorial será descrita uma aplicação simples para análise de sentimento do Twitter utilizando o Spark e o Kafka. Iremos utilizar a versão 1.5.1 do Spark e 0.8 do Kafka.

**Importante: antes de iniciar o tutorial mate qualquer processo que esteja rodando o Kafka em outra versão. Irá dar conflito com essa versão.**

## Configuração do projeto

### Inicializando o Kafka

Nesta seção iremos iniciar a estrutura do kafka. Primeiro faça o download do Kafka:

- Entre na pasta de Downloads e baixe o Kafka 0.8

```cd /home/etl/Downloads/big_data```

```wget https://archive.apache.org/dist/kafka/0.8.1.1/kafka_2.10-0.8.1.1.tgz```


- Descompacte o arquivo e entre na pasta do projeto

```tar -xvf kafka_2.10-0.8.1.1.tgz```

```cd kafka_2.10-0.8.1.1```

- Inicie o zookeeper:

```bin/zookeeper-server-start.sh config/zookeeper.properties```

- Iniciar o servidor Kafka:

```bin/kafka-server-start.sh config/server.properties```

- Crie um tópico no Kafka que irá receber os tweets com o comando:

```bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitterstream```

- Inicie o consumidor para ler os tweets que chegam no tópico twitterstream

```bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic twitterstream --from-beginning```

## Executando a aplicação de análise de sentimentos

### Configurando o projeto e instalando as dependências

Primeiro faça o download do Spark 1.5.1 com os passos abaixo:

```cd /home/etl/Downloads/big_data```

```wget https://d3kbcqa49mib13.cloudfront.net/spark-1.5.1-bin-hadoop2.6.tgz```

```tar -xvf spark-1.5.1-bin-hadoop2.6.tgz```

Para instalar todas as dependências, execute o script abaixo na pasta twitter-analysis:

``` cd /home/etl/Documentos/projetos/big_data/twitter_analysis_spark/twitter-analysis```

``` sudo ./install.sh ```

### Obtendo as chaves do Twitter

O script python app.py lê o stream de dados que chega do Twitter. Esse script irá precisar dos tokens de autenticação da sua conta no Twitter. Gere os tokens de acesso em: https://apps.twitter.com/ e atualize o arquivo `twitter-app-credentials.txt` com as chaves obtidas na api do Twitter. Siga este [tutorial](https://www.tutoriart.com.br/como-obter-consumer-key-secret-e-token-para-criar-aplicativos-do-twitter/) caso tenha alguma dúvida.

### Executando a aplicação de coleta de tweets

Inicie o download de tweets que serão enviados para o tópico twitterstream do Kafka com o comando abaixo dentro da pasta twitter-analysis:

```python app.py```

O código app.py coleta os tweets da api oficial do Twitter e envia para o tópico twitterstream do Kafka. Este código deve ficar rodando todo o tempo. Depois de iniciado essa aplicação, vá na tela do consumidor do Kafka e veja os tweets sendo impressos.

### Executando a aplicação de análise com Spark

A aplicação de análise de sentimentos do Twitter utilizando o Spark está no código twitterStream.py. Essa aplicação  recebe todas as mensagens publicadas no tópico twitterstream e conta o número de tweets com análise de sentimento positivo e negativo durante alguns minutos. Ao término desse tempo, a aplicação gera uma saída com o número de tweets positivos e negativos ao longo do tempo.

Para iniciar a aplicação digite o comando abaixo no terminal dentro da pasta do projeto:

```sudo /home/etl/Downloads/big_data/spark-1.5.1-bin-hadoop2.6/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.1 twitterStream.py```


# Análise dos tweets utilizando Spark e Kafka

Neste tutorial será descrita uma aplicação simples para análise de sentimento do Twitter utilizando o Spark e o Kafka. Iremos utilizar a versão 1.5.1 do Spark e 0.8 do Kafka.

**Importante: antes de iniciar o tutorial mate qualquer processo que esteja rodando o Kafka em outra versão. Irá dar conflito com essa versão.**

## Configuração do projeto

### Inicializando o Kafka

Nesta seção iremos iniciar a estrutura do kafka. Primeiro faça o download do Kafka:

- Entre na pasta de Downloads e baixe o Kafka 0.8

```cd /home/etl/Downloads```

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


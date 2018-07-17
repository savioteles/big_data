# Exemplo da integração do Flink com o Kafka usando dados de um Crawler

Este exemplo apresenta um crawler em python que envia dados para um tópico do Kafka que é consumido por um Stream Job do Flink desenvolvido em Java que realiza agregações e imprime o resultado na tela.

## Kafka

Siga as instruções abaixo:

- Baixe a versão 0.11.0.3 do Kafka no link: https://www.apache.org/dyn/closer.cgi?path=/kafka/0.11.0.3/kafka_2.11-0.11.0.3.tgz
- Descompacte em uma pasta local
- Abra a pasta descompactada do Kafka no terminal
- Inicie o Zookeeper com o comando:

	```bin/zookeeper-server-start.sh config/zookeeper.properties```
- Em outra aba do terminal, inicie o servidor do Kafka:

	```bin/kafka-server-start.sh config/server.properties```
- Em outra aba do terminal, crie o tópico farmacia e liste os tópicos (para verificar que foi criado) no Kafka com os dois comandos abaixo:

	```bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic farmacia```
	
	```bin/kafka-topics.sh --list --zookeeper localhost:2181```

## Flink
O job do Flink irá ler as mensagens do Kafka. Siga as instruções abaixo:
- Compile o projeto word-count, que é um projeto Maven com as dependências de biblioteca já configuradas.
- Execute a classe ReadFromKafka. Ela irá ler as mensagens que estão chegando no tópico farmacia do Kafka

## Crawler
O último passo é executar o crawler que irá ler as páginas web, extrair as informações desejadas e publicar no tópico farmacia do Kafka.

- Instale as dependências do Crawler executando o script **install.sh**:
	
	```./install.sh```

- No terminal, entre na pasta farmacia (que está na raiz deste projeto) e execute o seguinte comando:
	
	```scrapy crawl farmacia ```

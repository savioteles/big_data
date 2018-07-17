# Apache Flume

Vamos executar um tutorial com o seguinte arquivo de configuração do flume:

```
# Define a fonte, o canal e o sink
agent.sources = src2
agent.channels = chan2
agent.sinks = sink2

# Configura a fonte de dados para 'Spooling Directory' e configura o diretório que será lido
agent.sources.src2.type = spooldir
agent.sources.src2.spoolDir = /home/etl/Imagens
agent.sources.src2.basenameHeader = true
agent.sources.src2.deserializer=org.apache.flume.sink.solr.morphline.BlobDeserializer$Builder

# Configura o canal de troca de mensagens para a memória
agent.channels.chan2.type = memory
agent.channels.chan2.capacity = 1000

# Define o HDFS como 'sink' e configura o caminho do diretório de saída no HDFS
agent.sinks.sink2.type = hdfs
agent.sinks.sink2.hdfs.path = hdfs://localhost:9000/user/etl/flume
agent.sinks.sink2.hdfs.fileType = DataStream

# Disabilita as funcionalidades de 'rollover' para manter os arquivos originais
agent.sinks.sink2.rollCount = 0
agent.sinks.sink2.rollInterval = 0
agent.sinks.sink2.rollSize = 0
agent.sinks.sink2.idleTimeout = 0

# Configura o arquivo de saída com o mesmo de entrada
agent.sinks.sink2.hdfs.filePrefix = %{basename}

# Conecta fonte de dados e destino através do canal chan2
agent.sources.src2.channels = chan2
agent.sinks.sink2.channel = chan2
```

- Abra o terminao e inicie o flume:
	
	```cd Downloads/big_data/apache-flume-1.8.0-bin/```

- Execute o Apache Flume com o a configuração do stream acima (que está salvo no arquivo conf/example.conf)
	
	```bin/flume-ng agent --conf conf --conf-file conf/example.conf --name agent -Dflume.root.logger=INFO,console```


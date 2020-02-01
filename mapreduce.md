## Inserir arquivo no HDFS
hdfs dfs -put ~/Downloads/csv/assaults-2015-csv.csv hdfs://localhost:9000/user/etl

## Alterar Yarn
No arquivo /usr/local/hadoop/etc/hadoop/yarn-site.xml adicionar:
```
<property>
<name>yarn.nodemanager.vmem-check-enabled</name>
<value>false</value>
</property>
```

## Comando Spark
bin/spark-submit --master yarn-client --executor-memory 512M examples/src/main/python/wordcount.py /user/etl/assaults-2015-csv.csv

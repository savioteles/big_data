# Exemplo com o Sqoop

- Baixe o sqoop no link http://mirror.nbtelecom.com.br/apache/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
- Descompacte o arquivo na pasta Downloads
- Abra o terminal e digite:

    ```cd ~/Downloads/big_data/sqoop-1.4.7.bin__hadoop-2.6.0```

- Instalar driver postgres
    -- Baixar o jar https://jdbc.postgresql.org/download/postgresql-42.2.4.jar
    -- Colocar o jar dentro da pasta do sqoop (~/Downloads/sqoop-1.4.7.bin__hadoop-2.6.0)

- Listar Tabelas para ver se está funcionando a integração com o Postgres
    
    ```bin/sqoop list-tables --connect jdbc:postgresql://localhost/postgres --username postgres --password postgres --driver org.postgresql.Driver```

- Importar os dados do postgres no HDFS

    ```bin/sqoop import --connect jdbc:postgresql://localhost/postgres --username postgres --password postgres --driver org.postgresql.Driver --table orders_sale -m 1 --target-dir /fasam/orders_sale```

- Importar os dados utilizando uma consulta como restrição
    
    ```bin/sqoop import --query "select * from orders_sale where ship_mode='Regular Air' AND \$CONDITIONS" --connect jdbc:postgresql://localhost/postgres --username postgres --password postgres --driver org.postgresql.Driver -m 1 --target-dir /fasam/orders_sale_query```

- Importar somente as colunas row_id e sales
    
    ```bin/sqoop import --columns "row_id,sales" --connect jdbc:postgresql://localhost/postgres --username postgres --password postgres --driver org.postgresql.Driver --table orders_sale -m 1 --target-dir /fasam/orders_sale_columns```

- Importação dos dados mudando o paralelismo de 1 para 4

    ```bin/sqoop import --connect jdbc:postgresql://localhost/postgres --username postgres --password postgres --driver org.postgresql.Driver --table orders_sale -m 4 --split-by row_id --target-dir /fasam/orders_sale_paralle```


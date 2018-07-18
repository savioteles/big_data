# ETL com Pentaho

Neste projeto apresentamos um exemplo de ETL utilizando o Pentaho. Neste exemplo, é realizada uma extração dos dados de empregados de hospitais públicos da cidade de São Paulo (que estão no arquivo csv */home/etl/Documentos/projetos/big_data/pentaho/folha_hospital.csv*) e são realizadas as seguintes transformações:

- Cálculo da idade de cada empregado do hospital
- Cálculo do tempo de serviço em anos
- Mapeamento do campo vinculo para um campo inteiro
	- Estatutário: servidor público (estatuto do servidor público municipal) -> 0
	- CLT: contrato por tempo indeterminado -> 1
	- Residência Médica -> 2
	- Servidor público cedido por outro ente: Servidor Público Municipal -> 3
	- Desligado -> 4

O resultado é escrito na tabela hospital_result no Postgres. A pasta sql contém o arquivo create_table_postgres_result.sql utilizado para criar a tabela de saída no Postgres.

Para abrir o Pentaho entre o comando abaixo:

```
cd /home/etl/Downloads/data-integration/
./spoon.sh
```

Dentro do Pentaho importe a transformação hospital.ktr que está em */home/etl/Documentos/projetos/big_data/pentaho/hospital.ktr*. 

Execute a transformação no Pentaho e veja o resultado da importação abrindo o PgAdmin 3 e olhando as tuplas na tabela hospital_result no Postgres.


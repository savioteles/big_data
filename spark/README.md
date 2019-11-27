# Apache Spark

Este tutorial tem como objetivo facilitar o entendimento do conceito de Big Data utilizando o Apache Spark no ambiente da Databricks.

Os arquivos com extensão .ipynb neste projeto apresentam exemplos análises de dados com métodos de leitura, transformação e escrita dos dados utilizando o Apache Spark. Estes arquivos podem ser importados em diversas ferramentas, tais como [Jupyter](https://jupyter.org/), [Pycharm](https://www.jetbrains.com/pycharm/) e na plataforma da [Databricks](https://community.cloud.databricks.com/).

A plataforma community da Databricks é free e você pode criar sua conta no link https://community.cloud.databricks.com. Depois de criada a conta, é possível importar os arquivos .ipynb utilizando o tutorial disponível na plataforma (https://docs.databricks.com/notebooks/notebooks-manage.html).


## Arquitetura do Apache Spark na plataforma Databricks
Antes de partir para o código, vamos ver uma visão geral da arquitetura do Apache Spark. Esta arquitetura permite que você possa processar seus códigos em várias máquinas como se fosse uma só através da arquitetura master-worker, onde existe um `driver` ou nó master no cluster, acompanhado pelos nós `worker`. O master envia o trabalho para os workers com instruções para carregar os dados da memória ou do disco.

O diagrama abaixo apresenta um exemplo de um cluster com Apache Spark, onde basicamente existe um nó Driver que comunica com os nós executors. Cada um destes nós executors tem slots que são logicamente como núcleos de processsamento.

![spark-architecture](http://training.databricks.com/databricks_guide/gentle_introduction/videoss_logo.png)

O Driver envia Tasks para os slots vazios nos Executors quando o trabalho estiver terminado:

![spark-architecture](http://training.databricks.com/databricks_guide/gentle_introduction/spark_cluster_tasks.png)

Nota: No caso da edição Community da plataforma Databricks, não existe Worker e o Master fica responsável por executar o código inteiro:

![spark-architecture](http://training.databricks.com/databricks_guide/gentle_introduction/notebook_microcluster.png)

Você pode visualizar os detalhes da sua aplicação na interface web do Apache Spark acessível na plataforma Databricks clicando "Clusters" e então no link "Spark UI". O link também está disponível no canto superior esquerdo deste notebook onde você pode selecionar o cluster que está ligado (Attached) a este notebook.

package stream_analytics.word_count;

/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer011;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.tuple.Tuple2;

import java.util.Properties;

public class ReadFromKafka {

	public static void main(String[] args) throws Exception {
		// Criar o ambiente de execução
		StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

		// Configura as propriedades de comunicação com o Kafka, como o endereço do servidor do Kafka e o grupo de consumidor deste job
		Properties properties = new Properties();
		properties.setProperty("bootstrap.servers", "localhost:9092");
		properties.setProperty("group.id", "flink_consumer");

		// Cria um stream que irá escutar todas as mensagens que chegam no tópico 'farmacia'. 
		// Cada mensagem é transofrmada em String;
		DataStream<String> stream = env
				.addSource(new FlinkKafkaConsumer011<>("farmacia", new SimpleStringSchema(), properties));

		// Constroi o fluxo de execução do stream que irá contar o número de medicamentos por cada marca em um intervalo de 10 segundos
		stream.map(new MapFunction<String, Tuple2<String, Integer>>() {
			private static final long serialVersionUID = -6867736771747690202L;

			@Override
			public Tuple2<String, Integer> map(String value) throws Exception {
				// Obtém os dados do medicamento, faz o split por ';' e pega a marca do medicamento
				String[] dadosMedicamento = value.split(";");
				String marcaMedicamento = dadosMedicamento[1];
				// Retorna a marca do medicamento e o número 1 para contar mais um medicamento desta marca foi encontrado
				return new Tuple2<String, Integer>(marcaMedicamento, 1);
			}
		})
		.keyBy(0)	//agrega pela marca de medicamento (que é a chave -posição 0- no objeto Tuple2<String, Integer>)
		.timeWindow(Time.seconds(10))	//agrega os resultados em uma janela de tempo de 10 segundos
		.sum(1)		// Faz a soma do número de medicamentos (que é o valor -posição 1- no objeto Tuple2<String, Integer>)
		.print();	// Imprime o resultado na tela

		// Executa o plano definido acima no Flink.
		env.execute();
	}

}

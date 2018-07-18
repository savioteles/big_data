# -*- coding: utf-8 -*-
# biblioteca que vamos utilizar para extrair dados de uma página web
import scrapy
# biblioteca cliente do Apache Kafka
from kafka import SimpleProducer, KafkaClient

class FarmaciaSpider(scrapy.Spider):
    def __init__(self):
        super(scrapy.Spider, self).__init__()
        client = KafkaClient("localhost:9092")
        # O produtor de mensagens para o Kafka é iniciado apontando para o servidor do Kafka que está escutando localmente na porta 9092
        self.producer = SimpleProducer(client, async = True,
                          batch_send_every_n = 1000,
                          batch_send_every_t = 10)

    # nome do spider que é utilizado na inicialização do Spider (scrapy crawl *farmacia*)
    name = "farmacia"
    # Domínios que serão acessados pelo crawler
    allowed_domains = ["drogaraia.com.br"]
    start_urls = (
        'http://www.drogaraia.com.br/saude/medicamentos/todos-de-a-z.html?p=5',
    )

    def parse(self, response):
        # Para cada página web de resposta devemos fazer o parser. Vamos buscar as informações dos medicamentos e olhando para o HTML estas informações vem nas divs com class product-info
        medicamentos = response.xpath('//div[@class="product-info"]')
        for medicamento in medicamentos:
            # Como são vários médicamentos com a class="product-info", percorremos cada um buscando seus atributos. O primeiro é o nome do medicamento que no HTML está na class="product-name" no atributo title de <a>
            nome_medicamento = medicamento.xpath('div[@class="product-name"]/a/@title').extract_first().encode('utf-8')
            if nome_medicamento is not None:
                print "Nome do medicamento: " +nome_medicamento
                # Agora busca os detalhes dos medicamentos que serão utilizados como dados a serem enviados para o Kafka
                detalhes_medicamento = medicamento.xpath('div[@class="product-attributes"]')
                # A marca do medicamento está no texto HTML na class "marca". 
                # Repare que aqui estamos utilizando o contains para encontrar a class, ou seja, 
                # qualquer class que tenha essa class e extraimos a primeira que encontramos.
                marca = detalhes_medicamento.xpath('.//li[contains(@class, "marca")]/text()').extract_first().encode('utf-8')
                print "Marca: " +marca
                # A quantidade do medicamento está no texto HTML na class "quantidade show".
                quantidade = detalhes_medicamento.xpath('.//li[contains(@class, "quantidade show")]/text()').extract_first().encode('utf-8')
                print "Quantidade: " +quantidade
                # O principio ativo do medicamento está no texto HTML na class "principioativo show".
                principio_ativo = detalhes_medicamento.xpath('.//li[contains(@class, "principioativo show")]/text()').extract_first(default='not-found').encode('utf-8')
                print "Princípio ativo: " +principio_ativo
                # O preço do medicamento está no texto HTML na propriedade "price". Se não for encontrado o preço do medicamento, colocamos o valor '0' como padrão.
                preco_atual = medicamento.xpath('.//span[@property="price"]/text()').extract_first(default='0').encode('utf-8')
                print "Preço atual: R$ " +preco_atual
                # Montamos o corpo da mensagem que será enviada para o tópico do Kafka
                dados_medicamento = nome_medicamento +";" + marca +";" +quantidade +";" +principio_ativo +";" +preco_atual
                print "Dados do medicamento: " +dados_medicamento
                # Enviamos a mensagem para o tópico farmacia. Todos que estiverem escutando neste tópico do Kafka irão receber a mensagem.
                self.producer.send_messages(b'farmacia', dados_medicamento)
        # Obtém o link da próxima página buscando a url que está apontando o botão "Próximo" na página HTML
        next_page = response.xpath('//li[contains(@class, "current inline")]/text()').extract_first()
        url_np = response.xpath('//a[contains(@class, "next i-next btn-more")]/@href').extract_first(default='not-found').encode('utf-8').strip()
        
        if url_np:
            # Inicia o crawler da próxima página e retorna.
            cookie = response.headers
            request = scrapy.Request(url=url_np, headers={'Cookie': cookie}, callback=self.parse)
            yield request

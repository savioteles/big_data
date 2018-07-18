CREATE EXTERNAL TABLE hospital (empresa string,mes string,ano int,nome string,cargo string,lotacao string,admissao date,nascimento int,vencimentos double,encargos double,beneficios double,outras int,vinculo string,idade int, tempo_servico int, vinculo_code int)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/fasam/hospital';
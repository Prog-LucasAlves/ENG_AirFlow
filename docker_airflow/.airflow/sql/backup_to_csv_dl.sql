COPY (SELECT * FROM {{ params.table }}) TO '/var/transfer/moedas.csv'  WITH CSV HEADER DELIMITER ';' ENCODING 'UTF-8'

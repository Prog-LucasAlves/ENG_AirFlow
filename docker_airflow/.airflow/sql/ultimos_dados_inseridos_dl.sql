COPY (SELECT * FROM {{ params.table }} where 
create_date > (NOW() - interval '5 minute')) TO '/var/transfer/moedas_unicos.csv'  WITH CSV HEADER DELIMITER ';' ENCODING 'UTF-8'
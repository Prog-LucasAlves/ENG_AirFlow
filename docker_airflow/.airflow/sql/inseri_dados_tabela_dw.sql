COPY {{ params.table }} (id, code, codein, name, high, low, varbid, pctchange, bid, ask, create_date) FROM {{ params.path }}  WITH DELIMITER AS ';' CSV HEADER

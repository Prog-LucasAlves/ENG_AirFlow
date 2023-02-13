DELETE FROM {{ params.table }} a USING (SELECT MIN(ctid) AS ctid, code, codein ,create_date
                                   FROM {{ params.table }} 
                                        GROUP BY code, codein, create_date HAVING COUNT(*) > 1) b 
                                                 WHERE a.code = b.code 
                                                       AND a.ctid <> b.ctid
                                                       AND a.codein = b.codein
                                                       AND a.ctid <> b.ctid
                                                       AND a.create_date = b.create_date 
                                                       AND a.ctid <> b.ctid

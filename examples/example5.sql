SELECT
    CASE WHEN id = 1 
         THEN "OneOrMA"
         ELSE
             CASE WHEN state = 'MA' THEN "OneOrMA" ELSE "NotOneOrMA" END
    ENd AS IdRedux
FROM customer
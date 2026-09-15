-- ============================================================

-- Constroi um calendario cobrindo todo o periodo de dados e cruza
-- com as vendas de lojas fisicas (pos), tratando dias sem venda
-- como zero -- corrigindo o vies de media que ignorava esses dias

-- ============================================================

WITH calendario AS (
    SELECT generate_series(
        (SELECT MIN(created_at::date) FROM orders),
        (SELECT MAX(created_at::date) FROM orders),
        '1 day'::interval
    )::date AS data
),

vendas_por_dia AS (
    -- soma o valor vendido por dia, so das lojas fisicas (pos)
    SELECT
        created_at::date AS data,
        SUM(total) AS valor_venda
    FROM orders
    WHERE channel = 'pos'
    GROUP BY created_at::date
),

calendario_vendas AS (
    -- LEFT JOIN: mantem TODOS os dias do calendario, mesmo os que
    -- nao tem nenhuma linha em vendas_por_dia (dias sem venda)
    SELECT
        c.data,
        COALESCE(v.valor_venda, 0) AS valor_venda,
        CASE EXTRACT(ISODOW FROM c.data)
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terca-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sabado'
            WHEN 7 THEN 'Domingo'
        END AS dia_semana
    FROM calendario c
    LEFT JOIN vendas_por_dia v ON v.data = c.data
)

SELECT
    dia_semana,
    ROUND(AVG(valor_venda), 2) AS media_vendas,
    COUNT(*) AS qtd_dias_no_periodo
FROM calendario_vendas
GROUP BY dia_semana
ORDER BY media_vendas ASC;
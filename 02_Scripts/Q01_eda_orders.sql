-- ============================================================

-- Tabela orders, calculando o volume, o intervalo de datas da 
-- coluna created_at e as estatísticas da coluna total

-- ============================================================
SELECT

    COUNT(*) AS total_linhas,
    MIN(created_at) AS data_minima,
    MAX(created_at) AS data_maxima,
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    AVG(total) AS valor_medio
FROM orders;
-- 48998	"2020-01-01 01:19:28"	"2026-12-31 23:43:09"	32.62	127262.02	28704.992077227642

-- Quantidade de colunas (consulta ao dicionario de dados do Postgres)
SELECT COUNT(*) AS total_colunas
FROM information_schema.columns
WHERE table_name = 'orders';
 
-- Checagem de duplicidade de id
SELECT
    COUNT(*) AS total_linhas,
    COUNT(DISTINCT id) AS ids_unicos,
    COUNT(*) - COUNT(DISTINCT id) AS linhas_duplicadas
FROM orders;
 
-- Consistencia aritmetica: subtotal - discount_amount deve ser = total
SELECT COUNT(*) AS linhas_inconsistentes
FROM orders
WHERE ABS((subtotal - discount_amount) - total) > 0.01;
 
-- Nulos por coluna-chave
SELECT
    COUNT(*) FILTER (WHERE salesperson_id IS NULL) AS nulos_salesperson_id,
    COUNT(*) FILTER (WHERE customer_id  IS NULL) AS nulos_customer_id,
    COUNT(*) FILTER (WHERE total        IS NULL) AS nulos_total
FROM orders;
 
-- Padrao do nulo em salesperson_id: cruza com o canal de venda
SELECT
    channel,
    COUNT(*) AS total_pedidos,
    COUNT(*) FILTER (WHERE salesperson_id IS NULL) AS nulos_salesperson
FROM orders
GROUP BY channel;
 
-- Outliers em "total" via metodo IQR
WITH quartis AS (
    SELECT
        percentile_cont(0.25) WITHIN GROUP (ORDER BY total) AS q1,
        percentile_cont(0.75) WITHIN GROUP (ORDER BY total) AS q3
    FROM orders
),
limites AS (
    SELECT
        q1, q3, (q3 - q1) AS iqr,
        q1 - 1.5 * (q3 - q1) AS limite_inferior,
        q3 + 1.5 * (q3 - q1) AS limite_superior
    FROM quartis
)
SELECT
    l.limite_inferior,
    l.limite_superior,
    (SELECT COUNT(*) FROM orders o WHERE o.total > l.limite_superior) AS qtd_acima_limite
FROM limites l;
 
-- Distribuicao de status (base para decisao de excluir cancelled/draft)
SELECT
    status,
    COUNT(*) AS quantidade,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentual
FROM orders
GROUP BY status
ORDER BY quantidade DESC;
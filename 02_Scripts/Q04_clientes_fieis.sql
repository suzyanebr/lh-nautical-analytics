-- ============================================================

-- Identifica os 10 clientes "fieis" (ticket medio alto + diversidade
-- de categorias >= 13) e a categoria de produto que esse grupo mais
-- compra em quantidade de itens.
--
-- Cadeia de chaves: orders.customer_id -> orders.id = order_items.order_id
--   -> order_items.product_variant_id = product_variants.id
--   -> product_variants.product_id = products.id
--   -> products.category_id = categories.id

-- ============================================================

WITH metrica_pedidos AS (
    -- Faturamento Total e Frequencia por cliente, direto da tabela orders
    SELECT
        customer_id,
        SUM(total) AS faturamento_total,
        COUNT(id)  AS frequencia
    FROM orders
    GROUP BY customer_id
),

diversidade_categorias AS (
    -- Quantas categorias DISTINTAS cada cliente ja comprou.
    -- Precisa "descer" da orders ate categories atraves da cadeia
    -- de chaves estrangeiras (join encadeado)
    SELECT
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi      ON oi.order_id = o.id
    JOIN product_variants pv ON pv.id = oi.product_variant_id
    JOIN products p          ON p.id = pv.product_id
    GROUP BY o.customer_id
),

metrica_cliente AS (
    -- Junta as duas metricas acima e calcula o Ticket Medio
    SELECT
        mp.customer_id,
        mp.faturamento_total,
        mp.frequencia,
        ROUND(mp.faturamento_total / mp.frequencia, 2) AS ticket_medio,
        dc.diversidade_categorias
    FROM metrica_pedidos mp
    JOIN diversidade_categorias dc ON dc.customer_id = mp.customer_id
),

top10_fieis AS (
    -- Filtro de elite: so entram clientes com diversidade >= 13
    -- Ordena por ticket medio desc; em caso de empate, customer_id asc
    SELECT *
    FROM metrica_cliente
    WHERE diversidade_categorias >= 13
    ORDER BY ticket_medio DESC, customer_id ASC
    LIMIT 10
),

categoria_mais_comprada AS (
    SELECT
        cat.name AS categoria,
        SUM(oi.quantity) AS quantidade_total_itens
    FROM top10_fieis t
    JOIN orders o             ON o.customer_id = t.customer_id
    JOIN order_items oi        ON oi.order_id = o.id
    JOIN product_variants pv   ON pv.id = oi.product_variant_id
    JOIN products p            ON p.id = pv.product_id
    JOIN categories cat        ON cat.id = p.category_id
    GROUP BY cat.name
    ORDER BY quantidade_total_itens DESC
    LIMIT 1
)

SELECT
    t.customer_id,
    t.faturamento_total,
    t.frequencia,
    t.ticket_medio,
    t.diversidade_categorias,
    (SELECT categoria FROM categoria_mais_comprada)             AS categoria_mais_comprada_pelo_grupo,
    (SELECT quantidade_total_itens FROM categoria_mais_comprada) AS qtd_itens_dessa_categoria
FROM top10_fieis t
ORDER BY t.ticket_medio DESC, t.customer_id ASC;
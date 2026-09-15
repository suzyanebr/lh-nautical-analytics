"""
Constroi uma matriz de interacao Usuario x Produto (1 = o cliente
ja comprou o produto ao menos uma vez, 0 = nunca comprou -- a
quantidade comprada e ignorada de proposito), calcula a
Similaridade de Cosseno entre produtos com base em quais clientes
compraram cada um, e gera um ranking dos produtos mais parecidos
com um produto de referencia.

"""
 
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity

# Garante que os CSVs sejam sempre lidos a partir da pasta onde este
# script esta salvo, nao importa de onde o terminal foi aberto
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))


def caminho(nome_arquivo):
    return os.path.join(PASTA_SCRIPT, nome_arquivo)


# ------------------------------------------------------------------
# 1. Carregar os dados e juntar as tabelas ate ter, em cada linha,
#    o par (customer_id, product_id) de uma compra
# ------------------------------------------------------------------

products = pd.read_csv(caminho("products.csv"))
variants = pd.read_csv(caminho("product_variants.csv"))
orders = pd.read_csv(caminho("orders.csv"))
order_items = pd.read_csv(caminho("order_items.csv"))

# order_items so tem product_variant_id -- precisa subir ate o
# product_id "pai" da variante
oi = order_items.merge(
    variants[["id", "product_id"]],
    left_on="product_variant_id",
    right_on="id",
    suffixes=("", "_variant"),
)

# e tambem precisa do customer_id, que esta em orders
oi = oi.merge(
    orders[["id", "customer_id"]],
    left_on="order_id",
    right_on="id",
    suffixes=("", "_order"),
)

interacoes = oi[["customer_id", "product_id"]].drop_duplicates()


# ------------------------------------------------------------------
# 2. Construir a matriz de interacao Usuario x Produto
#    Linhas = id_cliente, Colunas = id_produto
#    Valor = 1 se comprou ao menos uma vez, 0 caso contrario
# ------------------------------------------------------------------

matriz = pd.crosstab(interacoes["customer_id"], interacoes["product_id"])
matriz = (matriz > 0).astype(int)


# ------------------------------------------------------------------
# 3. Calcular a Similaridade de Cosseno entre PRODUTOS
#    (por isso transpomos a matriz: cada produto vira um vetor
#    de 2000 posicoes, uma por cliente)
# ------------------------------------------------------------------

similaridade = cosine_similarity(matriz.T)
similaridade_df = pd.DataFrame(
    similaridade, index=matriz.columns, columns=matriz.columns
)


# ------------------------------------------------------------------
# 4. Ranking dos 5 produtos mais similares a um produto de referencia
# ------------------------------------------------------------------

def top5_similares(nome_produto_referencia, produtos_df, similaridade_df):
    produto_ref = produtos_df[produtos_df["name"] == nome_produto_referencia]
    produto_ref_id = produto_ref["id"].iloc[0]

    similares = (
        similaridade_df[produto_ref_id]
        .drop(produto_ref_id)  # desconsidera o proprio produto no ranking
        .sort_values(ascending=False)
        .head(5)
    )

    nomes = produtos_df.set_index("id")["name"]
    resultado = pd.DataFrame({
        "product_id": similares.index,
        "nome": [nomes.get(pid, "???") for pid in similares.index],
        "similaridade": similares.values,
    })
    return resultado


ranking = top5_similares("Motor de Popa 1949", products, similaridade_df)
print("Top 5 produtos mais similares a 'Motor de Popa 1949':\n")
print(ranking.to_string(index=False))
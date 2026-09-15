"""

Modelo baseline: media movel dos ultimos 3 meses de vendas,
usando apenas dados anteriores a data prevista (sem vazamento
de dados futuros -- walk-forward).

Nota de qualidade de dados: existem DOIS produtos diferentes
com o nome exato "Bussola de Bordo 702" (id 74 e id 240) na
tabela products -- provavelmente uma colisao de nomes gerados
aleatoriamente. Como o enunciado identifica o produto pelo nome,
e nao pelo id, este script soma as vendas dos dois product_ids
que compartilham esse.

"""

import pandas as pd
import os

# Garante que os CSVs sejam sempre lidos a partir da pasta onde este
# script esta salvo, nao importa de onde o terminal foi aberto
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))


def caminho(nome_arquivo):
    return os.path.join(PASTA_SCRIPT, nome_arquivo)


# ------------------------------------------------------------------
# 1. Carregar os datasets exigidos e montar a serie temporal mensal
#    de quantidade vendida do produto alvo
# ------------------------------------------------------------------

products = pd.read_csv(caminho("products.csv"))
variants = pd.read_csv(caminho("product_variants.csv"))
orders = pd.read_csv(caminho("orders.csv"))
order_items = pd.read_csv(caminho("order_items.csv"))

NOME_PRODUTO = "Bússola de Bordo 702"

produto_alvo = products[products["name"] == NOME_PRODUTO]
variantes_alvo = variants[variants["product_id"].isin(produto_alvo["id"])]
itens_alvo = order_items[order_items["product_variant_id"].isin(variantes_alvo["id"])]

# junta com orders so para pegar a data do pedido (created_at)
itens_alvo = itens_alvo.merge(
    orders[["id", "created_at"]],
    left_on="order_id",
    right_on="id",
    suffixes=("", "_order"),
)
itens_alvo["created_at"] = pd.to_datetime(itens_alvo["created_at"])
itens_alvo["ano_mes"] = itens_alvo["created_at"].dt.to_period("M")

# soma de quantidade vendida por mes (essa e a "serie temporal" do produto)
serie_mensal = itens_alvo.groupby("ano_mes")["quantity"].sum().sort_index()


# ------------------------------------------------------------------
# 2. Modelo baseline: media movel dos ultimos 3 meses
#    (so usa dados anteriores ao mes que esta sendo previsto)
# ------------------------------------------------------------------

def prever_media_movel_3_meses(serie, mes_previsto):
    """
    Preve a quantidade de um mes usando a media simples dos 3 meses
    imediatamente anteriores a ele. Se um mes da janela nao existir
    na serie (sem vendas registradas), conta como 0 -- e nao vaza
    nenhum dado do mes previsto ou de meses posteriores.
    """
    janela = [mes_previsto - 3, mes_previsto - 2, mes_previsto - 1]
    valores = [serie.get(mes, 0) for mes in janela]
    return sum(valores) / 3


# ------------------------------------------------------------------
# 3. Gerar a previsao mensal para o periodo de teste (Q1 2026)
# ------------------------------------------------------------------

meses_teste = [pd.Period("2026-01", freq="M"),
               pd.Period("2026-02", freq="M"),
               pd.Period("2026-03", freq="M")]

previsoes = {}
valores_reais = {}

for mes in meses_teste:
    previsoes[mes] = prever_media_movel_3_meses(serie_mensal, mes)
    valores_reais[mes] = serie_mensal.get(mes, 0)


# ------------------------------------------------------------------
# 4. Comparar previsao x real usando MAE (Mean Absolute Error)
# ------------------------------------------------------------------

erros_absolutos = [abs(valores_reais[m] - previsoes[m]) for m in meses_teste]
mae = sum(erros_absolutos) / len(erros_absolutos)

soma_prevista_trimestre = sum(previsoes.values())

print("Previsao por mes (baseline - media movel 3 meses):")
for mes in meses_teste:
    print(f"  {mes}: previsto={previsoes[mes]:.2f}  real={valores_reais[mes]}")

print(f"\nSoma prevista para o 1o trimestre de 2026 (arredondada): {round(soma_prevista_trimestre)}")
print(f"MAE (Mean Absolute Error): {mae:.2f}")


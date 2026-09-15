"""

LH Nautical - Geracao automatica de schema PostgreSQL a partir de CSVs
Objetivo: ler todos os CSVs de um diretorio, detectar o tipo de cada
coluna e gerar um unico arquivo schema.sql com os CREATE TABLE para
PostgreSQL.

"""

import csv
import os
from datetime import datetime

# ajuste este caminho para a pasta onde estao os 24 CSVs
CSV_DIR = "."
OUTPUT_FILE = "schema.sql"


# ------------------------------------------------------------------
# Funcoes de teste de tipo
# Cada uma tenta converter um valor (string) para um tipo especifico.
# Se der certo -> True. Se der erro -> False.
# ------------------------------------------------------------------

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# limites do tipo INTEGER no Postgres (4 bytes, com sinal)
INTEGER_MIN = -2147483648
INTEGER_MAX = 2147483647

# limites do tipo BIGINT no Postgres (8 bytes, com sinal)
BIGINT_MIN = -9223372036854775808
BIGINT_MAX = 9223372036854775807


def cabe_em_integer(valores_int):
    """
    Recebe uma lista de valores ja convertidos para int e checa se
    TODOS cabem no intervalo do tipo INTEGER do Postgres.
    Se algum valor for maior (ex: CNPJ com 14 digitos, como tax_id),
    o Postgres rejeitaria a linha na hora de inserir os dados -- entao
    aqui a gente detecta isso ANTES, e usa BIGINT em vez de INTEGER.
    """
    return all(INTEGER_MIN <= v <= INTEGER_MAX for v in valores_int)


def cabe_em_bigint(valores_int):
    return all(BIGINT_MIN <= v <= BIGINT_MAX for v in valores_int)


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_bool(value):
    return value.upper() in ("TRUE", "FALSE")


def is_date(value):
    formatos = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in formatos:
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False


# ------------------------------------------------------------------
# Inferencia de tipo por coluna
# ------------------------------------------------------------------

def infer_column_type(values):
    """
    Recebe a lista de todos os valores (em texto) de UMA coluna e
    decide qual tipo SQL usar.

    A ordem do teste importa: um valor "1" passa tanto no teste de
    inteiro quanto no teste de texto, entao testamos do mais
    especifico (booleano) para o mais generico (texto), e so aceitamos
    um tipo se TODOS os valores nao-vazios da coluna passarem nele.
    """
    nao_vazios = [v for v in values if v != ""]

    if not nao_vazios:
        # coluna sem nenhum valor preenchido no arquivo inteiro
        return "TEXT"

    if all(is_bool(v) for v in nao_vazios):
        return "BOOLEAN"

    if all(is_int(v) for v in nao_vazios):
        valores_int = [int(v) for v in nao_vazios]
        if cabe_em_integer(valores_int):
            return "INTEGER"
        elif cabe_em_bigint(valores_int):
            return "BIGINT"
        else:
            # numero grande demais para qualquer tipo inteiro:
            # e um identificador (ex: chave de NF-e), nao uma quantidade
            return "TEXT"

    if all(is_float(v) for v in nao_vazios):
        return "NUMERIC(14,2)"

    if all(is_date(v) for v in nao_vazios):
        return "TIMESTAMP"

    return "TEXT"


# ------------------------------------------------------------------
# Geracao do CREATE TABLE
# ------------------------------------------------------------------

def gerar_create_table(nome_tabela, cabecalho, tipos_colunas):
    linhas = [f"CREATE TABLE {nome_tabela} ("]
    definicoes = []
    for coluna, tipo in zip(cabecalho, tipos_colunas):
        if coluna == "id":
            # convencao dos CSVs: a coluna "id" e sempre a chave primaria
            definicoes.append(f"    {coluna} {tipo} PRIMARY KEY")
        else:
            definicoes.append(f"    {coluna} {tipo}")
    linhas.append(",\n".join(definicoes))
    linhas.append(");")
    return "\n".join(linhas)


def processar_csv(caminho_arquivo):
    nome_tabela = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    with open(caminho_arquivo, newline="", encoding="utf-8") as f:
        leitor = csv.reader(f)
        cabecalho = next(leitor)

        # uma lista de valores para cada coluna, para depois inferir o tipo
        valores_por_coluna = [[] for _ in cabecalho]
        for linha in leitor:
            for i, valor in enumerate(linha):
                valores_por_coluna[i].append(valor)

    tipos_colunas = [infer_column_type(valores) for valores in valores_por_coluna]
    return gerar_create_table(nome_tabela, cabecalho, tipos_colunas)


# ------------------------------------------------------------------
# Execucao principal
# ------------------------------------------------------------------

def main():
    arquivos_csv = sorted(f for f in os.listdir(CSV_DIR) if f.endswith(".csv"))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as saida:
        for nome_arquivo in arquivos_csv:
            caminho = os.path.join(CSV_DIR, nome_arquivo)
            create_stmt = processar_csv(caminho)
            saida.write(create_stmt + "\n\n")
            print(f"Tabela gerada: {os.path.splitext(nome_arquivo)[0]}")

    print(f"\nArquivo '{OUTPUT_FILE}' gerado com sucesso.")


if __name__ == "__main__":
    main()

"""

Antes de rodar, instale a biblioteca de conexao (uma vez so):
    pip install psycopg2-binary

"""

import csv
import os
import psycopg2

# Forca as mensagens de erro do Postgres a virem em ingles (sem acentos).
# Isso evita um bug comum no Windows: quando a senha esta errada, o
# Postgres devolve a mensagem de erro em portugues (com "ç", "ã" etc),
# e o psycopg2 pode falhar ao decodificar esses caracteres, mostrando
# um UnicodeDecodeError confuso em vez do erro real de autenticacao.
os.environ["PGOPTIONS"] = "-c lc_messages=C"

# ------------------------------------------------------------------
# Dados de conexao com o banco.
# Isso e literalmente "a conexao" entre o Python e o Postgres: um
# conjunto de informacoes (endereco, porta, nome do banco, usuario,
# senha) que o psycopg2 usa para abrir um canal de comunicacao com
# o servidor Postgres que o pgAdmin tambem usa por baixo dos panos.
# ------------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "lh_nautical",
    "user": "postgres",
    "password": "SUA_SENHA_AQUI",  # a mesma senha que voce usa pra entrar no pgAdmin
}

# pasta onde estao os 24 CSVs (mesma pasta do script)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = BASE_DIR

# ordem de carga: nao ha FOREIGN KEY no schema gerado na Questao 2,
# entao a ordem das tabelas aqui nao afeta o resultado -- mas manter
# uma ordem fixa deixa o log de execucao mais facil de ler
TABELAS = [
    "addresses", "attributes", "brands", "categories", "customers",
    "employees", "fiscal_invoices", "goods_receipt_items", "goods_receipts",
    "locations", "order_items", "orders", "payments", "product_suppliers",
    "product_variants", "products", "purchase_order_items", "purchase_orders",
    "return_items", "returns", "stock_levels", "stock_movements",
    "suppliers", "variant_attribute_values",
]


def carregar_csv(cursor, nome_tabela):
    caminho_csv = os.path.join(CSV_DIR, f"{nome_tabela}.csv")

    with open(caminho_csv, newline="", encoding="utf-8") as f:
        leitor = csv.reader(f)
        cabecalho = next(leitor)

        colunas = ", ".join(cabecalho)
        marcadores = ", ".join(["%s"] * len(cabecalho))
        insert_sql = f"INSERT INTO {nome_tabela} ({colunas}) VALUES ({marcadores})"

        linhas = []
        for linha in leitor:
            # Em CSV, um campo vazio e representado como "" (string vazia).
            # No banco, "vazio" deve ser NULL, nao uma string vazia --
            # isso nao e "tratar" o dado, e apenas representar o mesmo
            # vazio corretamente no formato que o Postgres entende.
            linha_convertida = [valor if valor != "" else None for valor in linha]
            linhas.append(linha_convertida)

        cursor.executemany(insert_sql, linhas)
        return len(linhas)


def main():
    conexao = psycopg2.connect(**DB_CONFIG)
    cursor = conexao.cursor()

    print("Conectado ao banco. Iniciando carga...\n")

    for nome_tabela in TABELAS:
        try:
            qtd_linhas = carregar_csv(cursor, nome_tabela)
            conexao.commit()
            print(f"  {nome_tabela}: {qtd_linhas} linhas carregadas")
        except Exception as erro:
            conexao.rollback()
            print(f"  ERRO ao carregar '{nome_tabela}': {erro}")

    cursor.close()
    conexao.close()
    print("\nCarregamento finalizado.")


if __name__ == "__main__":
    main()
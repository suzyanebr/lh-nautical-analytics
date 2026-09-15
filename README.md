<img width="1500" height="800" alt="Image" src="https://github.com/user-attachments/assets/1bc0a92b-5796-4e76-aedf-7831df701f2a" />

# LH Nautical — Pipeline de Dados e Dashboard Analítico

## O problema
A LH Nautical (varejo náutico fictício) tinha 24 arquivos CSV brutos, sem tratamento, sem estrutura de banco e sem visão consolidada de vendas, clientes ou estoque. A diretoria precisava de respostas rápidas: quais clientes valem mais a pena reter, qual dia da semana realmente vende menos, e se dava pra prever a demanda de produtos-chave antes de faltar estoque.

## O que construí
Um pipeline completo, do dado bruto ao insight de negócio:

* **Engenharia de dados:** script Python (bibliotecas nativas) que lê os 24 CSVs, infere o tipo de cada coluna e gera o schema PostgreSQL automaticamente — detectando até anomalias como CNPJs que estouram o limite do tipo INTEGER
* **Carga de dados:** script de ingestão via `psycopg2`, tratando nulos corretamente sem alterar o dado original
* **SQL analítico:** consultas com CTEs encadeadas para segmentação de clientes (RFM simplificado) e uma dimensão de calendário construída do zero para corrigir um viés real de média (dias sem venda sendo ignorados no cálculo)
* **Machine Learning:** modelo baseline de previsão de demanda (média móvel) validado com MAE, e um sistema de recomendação baseado em similaridade de cosseno entre padrões de compra de clientes
* **Dashboard interativo em Power BI:** conectado direto ao PostgreSQL, com relacionamentos reais entre tabelas, medidas DAX e filtros cruzados — não são gráficos estáticos, os dados se atualizam entre si

## Principais achados
* Corrigi um erro clássico de análise: calcular média de vendas por dia da semana sem considerar dias sem venda inflava artificialmente o resultado. Com a correção, quinta-feira, não domingo, é o pior dia de vendas nas lojas físicas
* Os 10 clientes de maior ticket médio compram nas 14 categorias disponíveis — hélices é o produto que mais puxa esse grupo
* O modelo baseline erra por ~19 unidades (MAE) em produtos com pico de demanda repentino, evidenciando a necessidade de estoque de segurança

## Stack
`Python` (pandas, scikit-learn, psycopg2) · `PostgreSQL` · `SQL` (CTEs, window functions, dimensão de calendário) · `Power BI` (DAX, modelagem de dados)

## Estrutura do repositório
```text
/sql        -> scripts de EDA e análise de negócio
/python     -> geração de schema, carga de dados, ML
/dashboard  -> arquivo .pbix
README.md

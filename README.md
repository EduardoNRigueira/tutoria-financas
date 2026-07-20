# Finanças de Tutoria — Análise de Receita e Retenção

Projeto de portfólio em análise de dados: pipeline completo (geração/tratamento de
dados → SQL → Python/pandas → dashboard Power BI) aplicado a um negócio de tutoria
de matemática.

## Sobre os dados

Este é um **dataset sintético**, gerado com Python (`Faker` + regras de negócio
customizadas em `scripts/gerar_dataset.py`), simulando ~2,5 anos de aulas de um
tutor de matemática. Os dados não são reais, mas seguem padrões realistas de um
negócio desse tipo:

- Pico de demanda em períodos de prova (mar-abr, set-nov)
- Queda de demanda em férias escolares (dez-jan, jul)
- Taxa de falta (no-show) mais alta às segundas-feiras
- Alunos com tempo de permanência (churn) variável
- Preço por hora diferenciado por matéria

## Perguntas de negócio

1. Como a receita evolui mês a mês e por trimestre?
2. Quais matérias geram mais receita e têm o maior ticket médio?
3. Existe correlação entre dia da semana e taxa de falta?
4. Qual o tempo médio de retenção de um aluno?
5. Quais alunos estão "em risco" de abandono (sem aula há 60+ dias)?

## Principais insights

- Segunda-feira tem taxa de falta de **21,3%**, quase 4x maior que qualquer outro
  dia da semana — sugere ação prática: cobrar confirmação extra ou aplicar política
  de reagendamento específica para esse dia.
- Cálculo II e Álgebra Linear respondem por ~55% da receita total, com o maior
  ticket médio por aula.
- Receita trimestral cresce de forma sustentada, com quedas sazonais recorrentes
  em períodos de férias — útil para planejar fluxo de caixa.

## Stack

- **Python** (pandas, matplotlib, Faker) — geração, tratamento e EDA
- **SQL** (SQLite) — modelagem e KPIs (`sql/kpis.sql`)
- **Power BI** — dashboard interativo final

## Estrutura do repositório

```
tutoria-financas/
├── data/                  # CSVs brutos + banco SQLite
├── scripts/                # geração do dataset e carga no SQL
├── sql/kpis.sql            # queries de KPI
├── notebooks/               # análise exploratória em Python
├── dashboard/                # gráficos + CSVs prontos para Power BI
└── README.md
```

## Como rodar

```bash
pip install faker pandas matplotlib
python scripts/gerar_dataset.py
python scripts/carregar_sql.py
python notebooks/analise_exploratoria.py
```

## Dashboard

*(inserir aqui os prints do Power BI depois de montado — cartões de KPI,
receita mensal, receita por matéria, taxa de falta por dia)*

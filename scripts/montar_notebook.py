import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# ---------- Célula 1: Markdown - título ----------
cells.append(nbf.v4.new_markdown_cell(
"""# Análise Exploratória — Finanças de Tutoria

Este notebook carrega os dados do banco SQLite (`data/tutoria.db`), faz a
limpeza/tratamento em pandas e gera os gráficos usados no dashboard e no README.

**Dataset:** sintético, gerado com Faker + regras de negócio (ver `scripts/gerar_dataset.py`)."""
))

# ---------- Célula 2: Markdown - imports ----------
cells.append(nbf.v4.new_markdown_cell("## 1. Imports"))

# ---------- Célula 3: Código - imports ----------
cells.append(nbf.v4.new_code_cell(
"""import pandas as pd
import matplotlib.pyplot as plt
import sqlite3"""
))

# ---------- Célula 4: Markdown - carregar dados ----------
cells.append(nbf.v4.new_markdown_cell("## 2. Carregar dados do SQLite"))

# ---------- Célula 5: Código - carregar dados ----------
cells.append(nbf.v4.new_code_cell(
"""conn = sqlite3.connect("../data/tutoria.db")
aulas = pd.read_sql("SELECT * FROM aulas", conn, parse_dates=["data"])
alunos = pd.read_sql("SELECT * FROM alunos", conn, parse_dates=["entrada", "saida"])
conn.close()

print("Shape aulas:", aulas.shape)
aulas.head()"""
))

# ---------- Célula 6: Markdown - qualidade dos dados ----------
cells.append(nbf.v4.new_markdown_cell("## 3. Checagem de qualidade dos dados"))

# ---------- Célula 7: Código - checagem ----------
cells.append(nbf.v4.new_code_cell(
"""print(aulas.dtypes)
print()
print("Valores ausentes por coluna:")
print(aulas.isna().sum())"""
))

# ---------- Célula 8: Markdown - tratamento ----------
cells.append(nbf.v4.new_markdown_cell(
"""## 4. Tratamento

Cria colunas derivadas (mês, dia da semana) e isola só as aulas com status
`Realizada`, já que aulas canceladas/faltas não geram receita."""
))

# ---------- Célula 9: Código - tratamento ----------
cells.append(nbf.v4.new_code_cell(
"""aulas["mes"] = aulas["data"].dt.to_period("M").astype(str)
aulas["dia_semana"] = aulas["data"].dt.day_name()
realizadas = aulas[aulas["status"] == "Realizada"].copy()

realizadas.head()"""
))

# ---------- Célula 10: Markdown - receita mensal ----------
cells.append(nbf.v4.new_markdown_cell(
"""## 5. Receita mensal + média móvel

A média móvel de 3 meses ajuda a enxergar a tendência por trás da variação
mês a mês (que é bem ruidosa por causa da sazonalidade)."""
))

# ---------- Célula 11: Código - receita mensal ----------
cells.append(nbf.v4.new_code_cell(
"""receita_mensal = realizadas.groupby("mes")["valor"].sum().reset_index()
receita_mensal["media_movel_3m"] = receita_mensal["valor"].rolling(3).mean()

plt.figure(figsize=(10, 5))
plt.plot(receita_mensal["mes"], receita_mensal["valor"], marker="o", label="Receita mensal")
plt.plot(receita_mensal["mes"], receita_mensal["media_movel_3m"], linestyle="--", label="Média móvel (3m)")
plt.xticks(rotation=45, ha="right")
plt.title("Receita mensal da tutoria")
plt.ylabel("R$")
plt.legend()
plt.tight_layout()
plt.savefig("../dashboard/receita_mensal.png", dpi=120)
plt.show()"""
))

# ---------- Célula 12: Markdown - receita por matéria ----------
cells.append(nbf.v4.new_markdown_cell("## 6. Receita por matéria"))

# ---------- Célula 13: Código - receita por matéria ----------
cells.append(nbf.v4.new_code_cell(
"""receita_materia = realizadas.groupby("materia")["valor"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
receita_materia.plot(kind="barh")
plt.title("Receita total por matéria")
plt.xlabel("R$")
plt.tight_layout()
plt.savefig("../dashboard/receita_por_materia.png", dpi=120)
plt.show()

receita_materia"""
))

# ---------- Célula 14: Markdown - taxa de falta ----------
cells.append(nbf.v4.new_markdown_cell("## 7. Taxa de falta por dia da semana"))

# ---------- Célula 15: Código - taxa de falta ----------
cells.append(nbf.v4.new_code_cell(
"""taxa_falta = (
    aulas.groupby("dia_semana")["status"]
    .apply(lambda s: (s == "Falta").mean() * 100)
    .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
)
taxa_falta.index = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

plt.figure(figsize=(7, 5))
taxa_falta.plot(kind="bar", color="indianred")
plt.title("Taxa de falta (%) por dia da semana")
plt.ylabel("% de faltas")
plt.tight_layout()
plt.savefig("../dashboard/taxa_falta_dia.png", dpi=120)
plt.show()

taxa_falta"""
))

# ---------- Célula 16: Markdown - retenção ----------
cells.append(nbf.v4.new_markdown_cell("## 8. Retenção: tempo de permanência dos alunos"))

# ---------- Célula 17: Código - retenção ----------
cells.append(nbf.v4.new_code_cell(
"""alunos["meses_ativo"] = (alunos["saida"] - alunos["entrada"]).dt.days / 30

plt.figure(figsize=(7, 5))
alunos["meses_ativo"].plot(kind="hist", bins=10, color="steelblue", edgecolor="white")
plt.title("Distribuição do tempo de permanência dos alunos (meses)")
plt.xlabel("Meses ativo")
plt.tight_layout()
plt.savefig("../dashboard/retencao_alunos.png", dpi=120)
plt.show()

print("Média de meses ativo:", round(alunos["meses_ativo"].mean(), 1))"""
))

# ---------- Célula 18: Markdown - conclusão ----------
cells.append(nbf.v4.new_markdown_cell(
"""## 9. Principais insights

- Segunda-feira tem taxa de falta muito acima da média dos outros dias.
- Duas matérias concentram mais da metade da receita total.
- Receita cresce de forma sustentada, com quedas sazonais recorrentes em
  períodos de férias escolares."""
))

nb["cells"] = cells

with open("/home/claude/tutoria-financas/notebooks/analise_exploratoria.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Notebook criado com", len(cells), "células.")

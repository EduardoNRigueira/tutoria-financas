"""Carrega alunos.csv e aulas.csv em um banco SQLite (data/tutoria.db)."""

import sqlite3
import csv

DB_PATH = "/home/claude/tutoria-financas/data/tutoria.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS aulas;

CREATE TABLE alunos (
    aluno_id TEXT PRIMARY KEY,
    materia_principal TEXT,
    entrada DATE,
    saida DATE,
    dia_preferido TEXT
);

CREATE TABLE aulas (
    aula_id INTEGER PRIMARY KEY,
    data DATE,
    aluno_id TEXT,
    materia TEXT,
    duracao_horas REAL,
    valor REAL,
    status TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(aluno_id)
);
""")

with open("/home/claude/tutoria-financas/data/alunos.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [(r["aluno_id"], r["materia_principal"], r["entrada"], r["saida"], r["dia_preferido"]) for r in reader]
    cur.executemany("INSERT INTO alunos VALUES (?,?,?,?,?)", rows)

with open("/home/claude/tutoria-financas/data/aulas.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (int(r["aula_id"]), r["data"], r["aluno_id"], r["materia"],
         float(r["duracao_horas"]), float(r["valor"]), r["status"])
        for r in reader
    ]
    cur.executemany("INSERT INTO aulas VALUES (?,?,?,?,?,?,?)", rows)

conn.commit()
print(f"OK: {len(rows)} aulas carregadas em {DB_PATH}")
conn.close()

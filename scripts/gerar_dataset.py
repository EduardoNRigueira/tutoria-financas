"""
Gerador de dataset sintético para o projeto "Finanças de Tutoria".

IMPORTANTE: este dataset é 100% simulado (Faker + regras de negócio),
criado para fins de portfólio. Isso é declarado explicitamente no
README do projeto -- não faz sentido esconder isso.

A ideia central: em vez de gerar valores aleatórios soltos, cada
registro de aula segue regras que imitam o comportamento real de um
negócio de tutoria de matemática:

- Mais aulas em períodos de prova (mar-abr, set-out-nov)
- Queda forte em dezembro/janeiro (férias escolares)
- Preço por hora varia por matéria (matérias mais "difíceis" custam mais)
- Taxa de falta (no-show) maior às segundas-feiras
- Alunos têm uma "vida útil" (churn): entram, ficam alguns meses, saem
- Leve tendência de crescimento de receita ao longo do tempo (efeito
  reputação/indicação)
"""

import random
from datetime import date, timedelta
import csv
from faker import Faker

fake = Faker("pt_BR")
random.seed(42)
Faker.seed(42)

# ---------- Configuração do domínio ----------

MATERIAS = {
    "Cálculo I":        (70, 90),
    "Cálculo II":       (75, 95),
    "Álgebra Linear":   (65, 85),
    "Matemática Básica": (50, 65),
    "Estatística":      (60, 80),
    "Geometria Analítica": (60, 80),
}

N_ALUNOS = 42
DATA_INICIO = date(2024, 2, 1)
DATA_FIM = date(2026, 6, 30)

# Meses de alta demanda (período de provas em faculdades no Brasil)
MESES_PICO = {3, 4, 9, 10, 11}
MESES_FERIAS = {12, 1, 7}  # férias/recesso -> queda de demanda

def gerar_alunos(n):
    alunos = []
    for i in range(1, n + 1):
        entrada = DATA_INICIO + timedelta(days=random.randint(0, 640))
        # "vida útil" do aluno: entre 1 e 14 meses de aulas
        duracao_meses = random.choices(
            [1, 2, 3, 4, 6, 8, 10, 14],
            weights=[10, 15, 20, 20, 15, 10, 6, 4],
        )[0]
        saida = min(entrada + timedelta(days=duracao_meses * 30), DATA_FIM)
        alunos.append({
            "aluno_id": f"A{i:03d}",
            "materia_principal": random.choice(list(MATERIAS.keys())),
            "entrada": entrada,
            "saida": saida,
            "dia_preferido": random.choice(
                ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
            ),
        })
    return alunos


def peso_demanda(d: date) -> float:
    """Fator multiplicador de chance de aula ocorrer, por época do ano."""
    if d.month in MESES_FERIAS:
        return 0.3
    if d.month in MESES_PICO:
        return 1.6
    return 1.0


def gerar_aulas(alunos):
    aulas = []
    aula_id = 1
    for aluno in alunos:
        preco_min, preco_max = MATERIAS[aluno["materia_principal"]]
        preco_hora = round(random.uniform(preco_min, preco_max), 2)

        # abordagem: iterar semana a semana a partir do dia preferido do aluno
        dia_semana_map = {
            "Segunda": 0, "Terça": 1, "Quarta": 2,
            "Quinta": 3, "Sexta": 4, "Sábado": 5,
        }
        alvo_weekday = dia_semana_map[aluno["dia_preferido"]]

        cursor = aluno["entrada"]
        # avança até o primeiro dia da semana certo
        while cursor.weekday() != alvo_weekday:
            cursor += timedelta(days=1)

        while cursor <= aluno["saida"]:
            chance_ocorrer = 0.8 * peso_demanda(cursor)
            chance_ocorrer = min(chance_ocorrer, 0.95)

            if random.random() < chance_ocorrer:
                # status da aula
                # segunda-feira tem taxa de falta maior
                chance_falta = 0.14 if alvo_weekday == 0 else 0.06
                chance_cancelamento = 0.05

                r = random.random()
                if r < chance_falta:
                    status = "Falta"
                elif r < chance_falta + chance_cancelamento:
                    status = "Cancelada"
                else:
                    status = "Realizada"

                duracao_horas = random.choice([1, 1, 1, 1.5, 2])

                # leve tendência de crescimento de preço ao longo do tempo
                meses_desde_inicio = (cursor.year - DATA_INICIO.year) * 12 + (
                    cursor.month - DATA_INICIO.month
                )
                fator_crescimento = 1 + (meses_desde_inicio * 0.006)
                valor = round(preco_hora * duracao_horas * fator_crescimento, 2)

                aulas.append({
                    "aula_id": aula_id,
                    "data": cursor.isoformat(),
                    "aluno_id": aluno["aluno_id"],
                    "materia": aluno["materia_principal"],
                    "duracao_horas": duracao_horas,
                    "valor": valor if status == "Realizada" else 0.0,
                    "status": status,
                })
                aula_id += 1

            cursor += timedelta(days=7)

    return aulas


def main():
    alunos = gerar_alunos(N_ALUNOS)
    aulas = gerar_aulas(alunos)

    with open("/home/claude/tutoria-financas/data/alunos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["aluno_id", "materia_principal", "entrada", "saida", "dia_preferido"])
        w.writeheader()
        for a in alunos:
            w.writerow(a)

    with open("/home/claude/tutoria-financas/data/aulas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["aula_id", "data", "aluno_id", "materia", "duracao_horas", "valor", "status"])
        w.writeheader()
        for a in aulas:
            w.writerow(a)

    print(f"Gerado: {len(alunos)} alunos, {len(aulas)} aulas.")


if __name__ == "__main__":
    main()

-- ============================================================
-- KPIs do projeto "Finanças de Tutoria"
-- ============================================================

-- 1. Receita mensal (só aulas realizadas)
SELECT
    strftime('%Y-%m', data) AS mes,
    ROUND(SUM(valor), 2) AS receita
FROM aulas
WHERE status = 'Realizada'
GROUP BY mes
ORDER BY mes;

-- 2. Receita total e ticket médio por matéria
SELECT
    materia,
    COUNT(*) AS aulas_realizadas,
    ROUND(SUM(valor), 2) AS receita_total,
    ROUND(AVG(valor), 2) AS ticket_medio
FROM aulas
WHERE status = 'Realizada'
GROUP BY materia
ORDER BY receita_total DESC;

-- 3. Taxa de falta (no-show) por dia da semana
SELECT
    CASE CAST(strftime('%w', data) AS INTEGER)
        WHEN 0 THEN 'Domingo' WHEN 1 THEN 'Segunda' WHEN 2 THEN 'Terça'
        WHEN 3 THEN 'Quarta' WHEN 4 THEN 'Quinta' WHEN 5 THEN 'Sexta'
        WHEN 6 THEN 'Sábado'
    END AS dia_semana,
    COUNT(*) AS total_aulas,
    SUM(CASE WHEN status = 'Falta' THEN 1 ELSE 0 END) AS faltas,
    ROUND(100.0 * SUM(CASE WHEN status = 'Falta' THEN 1 ELSE 0 END) / COUNT(*), 1) AS taxa_falta_pct
FROM aulas
GROUP BY dia_semana
ORDER BY taxa_falta_pct DESC;

-- 4. Retenção: tempo médio (em meses) que um aluno permanece ativo
SELECT
    ROUND(AVG(
        (julianday(saida) - julianday(entrada)) / 30.0
    ), 1) AS media_meses_retencao
FROM alunos;

-- 5. Receita por trimestre, para ver o efeito de sazonalidade (provas x férias)
SELECT
    strftime('%Y', data) || '-Q' ||
        ((CAST(strftime('%m', data) AS INTEGER) - 1) / 3 + 1) AS trimestre,
    ROUND(SUM(valor), 2) AS receita
FROM aulas
WHERE status = 'Realizada'
GROUP BY trimestre
ORDER BY trimestre;

-- 6. Alunos "em risco" de churn: sem aula realizada nos últimos 60 dias
-- mas com data de saída ainda no futuro em relação à última aula
SELECT
    a.aluno_id,
    a.materia_principal,
    MAX(u.data) AS ultima_aula
FROM alunos a
JOIN aulas u ON u.aluno_id = a.aluno_id AND u.status = 'Realizada'
GROUP BY a.aluno_id
HAVING julianday('2026-06-30') - julianday(ultima_aula) > 60
ORDER BY ultima_aula;

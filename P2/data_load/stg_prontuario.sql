/* Copiando dados das tabelas PACIENTE dos schemas dos hospitais a, b e c */
/* Hospital A */
INSERT INTO stg_prontuario.PACIENTE (nome, dt_nascimento, cpf, nome_mae, dt_atualizacao)
SELECT
    nome,
    dt_nascimento,
    cpf,
    nome_mae,
    dt_atualizacao
FROM stg_hospital_a.PACIENTE

UNION ALL

/* Hospital B */
SELECT
    nome,
    dt_nascimento,
    cpf,
    nome_mae,
    dt_atualizacao
FROM stg_hospital_b.PACIENTE

UNION ALL

/* Hospital C */
SELECT
    nome,
    dt_nascimento,
    cpf,
    nome_mae,
    dt_atualizacao
FROM stg_hospital_c.PACIENTE;
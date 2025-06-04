SELECT p.*
FROM stg_prontuario.PACIENTE p
INNER JOIN (
    SELECT
        cpf,
        MAX(dt_atualizacao) AS dt_atualizacao_mais_recente
    FROM stg_prontuario.PACIENTE
    GROUP BY cpf
    /* Retorna apenas pacientes que possuem duplicatas */
    /* HAVING COUNT(*) > 1 */
) AS ultima_atualizacao
ON p.cpf = ultima_atualizacao.cpf AND 
   p.dt_atualizacao = ultima_atualizacao.dt_atualizacao_mais_recente;
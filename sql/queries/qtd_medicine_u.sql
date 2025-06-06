SELECT
    REPLACE(FORMAT(AVG(qtd_prescricoes), 1), '.', ',') AS avg_medicamentos_u
FROM (
    SELECT
        ap.id_atend,
        COUNT(ap.id_prescricao) AS qtd_prescricoes
    FROM
        stg_prontuario.atendimento_prescricao ap
    JOIN
        stg_prontuario.atendimento a ON ap.id_atend = a.id
    WHERE
        a.tp_atend = 'U'
    GROUP BY
        ap.id_atend
) AS avg_medicamentos_u_query;
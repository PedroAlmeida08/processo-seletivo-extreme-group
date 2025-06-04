/* Encontra duplicatas na tabela PACIENTE do schema stg_prontuario, caso existam */
SELECT cpf, COUNT(*) AS quantidade_duplicatas
FROM stg_prontuario.PACIENTE
WHERE cpf IS NOT NULL
GROUP BY cpf
HAVING COUNT(*) > 1;
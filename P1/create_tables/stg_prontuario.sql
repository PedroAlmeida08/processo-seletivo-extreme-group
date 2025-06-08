/* Criação da tabela PACIENTE no schema stg_prontuario */
CREATE TABLE IF NOT EXISTS stg_prontuario.PACIENTE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    dt_nascimento DATE,
    cpf CHAR(11),
    nome_mae VARCHAR(255),
    /* Utilizar para dados fictícios */
    dt_atualizacao TIMESTAMP NOT NULL
    /* Utilizar para dados reais */
    /* dt_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL */
);
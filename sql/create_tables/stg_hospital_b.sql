/* Criação da tabela PACIENTE no schema stg_hospital_b */
CREATE TABLE IF NOT EXISTS stg_hospital_b.PACIENTE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    dt_nascimento DATE NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    nome_mae VARCHAR(255) NOT NULL,
    /* Utilizar para dados fictícios */
    dt_atualizacao TIMESTAMP NOT NULL
    /* Utilizar para dados reais */
    /* dt_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL */
);
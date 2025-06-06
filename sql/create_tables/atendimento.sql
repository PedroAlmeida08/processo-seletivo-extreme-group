CREATE TABLE IF NOT EXISTS stg_prontuario.atendimento(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    tp_atend CHAR(1) NOT NULL CHECK (tp_atend IN ('U', 'I', 'A'))
);
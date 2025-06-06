CREATE TABLE IF NOT EXISTS stg_prontuario.atendimento_prescricao(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    id_atend INT NOT NULL,
    id_prescricao INT NOT NULL,
    FOREIGN KEY (id_atend) REFERENCES stg_prontuario.atendimento(id)
    -- FOREIGN KEY (id_prescricao) REFERENCES Prescricao(id) -- 
);
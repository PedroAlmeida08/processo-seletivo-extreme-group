import csv

# --- Função para ler o arquivo de layout ---
def read_layout_file(layout_filepath):
    columns_info = []
    try:
        # newline='' para evitar problemas com quebras de linha em diferentes OS
        with open(layout_filepath, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            header = next(reader) # Pula o cabeçalho
            for row in reader:
                if len(row) >= 5:
                    col_name = row[0].strip()
                    col_size = int(row[1].strip())
                    col_start = int(row[2].strip()) - 1 # Ajusta para índice 0
                    col_end = int(row[3].strip())
                    col_type_sigtap = row[4].strip()

                    # Mapeando tipos SIGTAP para MySQL
                    mysql_type = f'VARCHAR({col_size})'
                    if 'NUMBER' in col_type_sigtap:
                        # Mapeamento para valores monetários
                        if col_name in ['VL_SH', 'VL_SA', 'VL_SP']:
                            mysql_type = 'DECIMAL(15,2)'
                        # Trocar para 'BIGINT' caso haja overflow
                        else:
                            mysql_type = 'INT'
                    
                    # Adiciona obrigatoriedade aos campos
                    mysql_type += ' NOT NULL'
                    
                    columns_info.append({
                        'name': col_name,
                        'size': col_size,
                        'start': col_start,
                        'end': col_end,
                        'sigtap_type': col_type_sigtap,
                        'mysql_type': mysql_type
                    })
    except FileNotFoundError:
        print(f"Erro: Arquivo de layout '{layout_filepath}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao analisar o layout '{layout_filepath}': {e}")
        return None
    return columns_info
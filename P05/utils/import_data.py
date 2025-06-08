import mysql.connector

# --- Função para popular tabelas com base nos arquivos lidos ---
def import_data(filepath, conn, table_name, columns_info):
    print(f"\nImportando arquivo: {filepath} para {table_name}")

    cursor = conn.cursor()
    
    # Prepara a instrução INSERT
    db_columns = []
    for col in columns_info:
        db_columns.append(col['name'])
    placeholders = ', '.join(['%s'] * len(db_columns))
    # Cria a estrutura do comando INSERT_INTO, mas ainda sem os valores (usando placeholders)
    insert_sql = f"INSERT INTO {table_name} ({', '.join(db_columns)}) VALUES ({placeholders})"

    # Insere em lotes para otimização
    batch_size = 1000
    data_to_insert = []
    
    try:
        # Codificação comum para arquivos SIGTAP é Latin-1
        with open(filepath, 'r', encoding='latin-1') as f:
            for i, line in enumerate(f):
                if not line.strip(): # Pula linhas vazias
                    continue
                
                values = []
                for col in columns_info:
                    try:
                        # Extrai a substring com base no início e fim do layout
                        no_typed_value = line[col['start']:col['end']].strip()
                        
                        # Converte para o tipo Python adequado
                        if 'NUMBER' in col['sigtap_type']:
                            if no_typed_value:
                                if col['name'] in ['VL_SH', 'VL_SA', 'VL_SP']:
                                    # Valores de custo, os 2 últimos dígitos são decimais e a outra parte da string é a parte inteira do número
                                    value = float(no_typed_value[:-2] + '.' + no_typed_value[-2:])
                                else:
                                    # Números gerais, converte para int
                                    value = int(no_typed_value)
                            else: # Tratamento de exceção caso haja um valor vazio para um campo NUMBER
                                value = None if 'NOT NULL' not in col['mysql_type'] else 0
                        else: # Qualquer outro que não seja NUMBER
                            if no_typed_value:
                                value = no_typed_value
                            else:
                                # Se a coluna MySQL permite NULL
                                if 'NOT NULL' not in col['mysql_type']: 
                                    # Atribui None (para mapear para NULL no DB)
                                    value = None
                                else:
                                    # Se a coluna MySQL é NOT NULL atribui string vazia para campos VARCHAR/CHAR NOT NULL 
                                    value = ''

                        values.append(value)

                    except (ValueError, IndexError) as e:
                        print(f"Aviso: Erro de processamento para campo '{col['name']}' ({col['sigtap_type']}) na linha {i+1} do arquivo '{filepath}': '{no_typed_value}'. Erro: {e}")
                        
                        # Adicionando valores à values para que a lista values não fique com um número de elementos menor do que o número de 
                        # colunas que a instrução INSERT espera. Isso pois, quando cursor.executemany(insert_sql, data_to_insert), se isso
                        # ocorrer, retornará um erro. 
                        if 'NOT NULL' not in col['mysql_type']:
                            values.append(None)
                        elif 'NUMBER' in col['sigtap_type']:
                            values.append(0)
                        else:
                            values.append('')
                
                data_to_insert.append(tuple(values))

                if (i + 1) % batch_size == 0:
                    try:
                        cursor.executemany(insert_sql, data_to_insert)
                        conn.commit()
                        print(f"   {i + 1} linhas processadas de '{filepath}'...")
                    except mysql.connector.Error as err_insert:
                        print(f"Erro ao inserir lote de dados na linha {i+1} de '{filepath}': {err_insert}")
                        conn.rollback()
                    data_to_insert = []
                        
            # Insere os dados restantes (que não formam um batch)
            if data_to_insert:
                try:
                    cursor.executemany(insert_sql, data_to_insert)
                    conn.commit()
                except mysql.connector.Error as err_final_insert:
                    print(f"Erro ao inserir lote final de dados de '{filepath}': {err_final_insert}")
                    conn.rollback()
            
        print(f"Arquivo '{filepath}' importado com sucesso!")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
    except Exception as e:
        print(f"Erro geral ao importar arquivo '{filepath}': {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

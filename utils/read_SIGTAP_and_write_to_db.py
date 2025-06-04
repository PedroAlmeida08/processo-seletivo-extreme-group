import os
import csv
import pandas as pd
import mysql.connector
from datetime import datetime

# --- Configurações do Banco de Dados MySQL ---
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'stg_prontuario',
    'user': 'joaosantos',
    'password': '123'
}

# --- Configurações dos Arquivos e Tabelas ---
DADOS_FOLDER = './data/sigtap-simplificado'
FILE_MAPPING = {
    'tb_procedimento.txt': {
        'layout_file': 'tb_procedimento_layout.txt',
        'table_name': 'stg_prontuario.sigtap_procedimento'
    },
    'rl_procedimento_cid.txt': {
        'layout_file': 'rl_procedimento_cid_layout.txt',
        'table_name': 'stg_prontuario.sigtap_rl_procedimento_cid'
    },
    'tb_grupo.txt': {
        'layout_file': 'tb_grupo_layout.txt',
        'table_name': 'stg_prontuario.sigtap_tb_grupo'
    },
    'tb_sub_grupo.txt': {
        'layout_file': 'tb_sub_grupo_layout.txt',
        'table_name': 'stg_prontuario.sigtap_tb_sub_grupo'
    },
    'tb_forma_organizacao.txt': {
        'layout_file': 'tb_forma_organizacao_layout.txt',
        'table_name': 'stg_prontuario.sigtap_tb_forma_organizacao'
    },
    'tb_cid.txt': {
        'layout_file': 'tb_cid_layout.txt',
        'table_name': 'stg_prontuario.sigtap_tb_cid'
    }
}

# --- Função para conectar ao banco de dados ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Conexão com o banco de dados MySQL estabelecida com sucesso!")
            return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados MySQL: {err}")
        return None

# --- Função para ler o arquivo de layout ---
def parse_layout_file(layout_filepath):
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

# --- Função para criar a tabela com base no layout ---
def create_table_from_layout(cursor, table_name, columns_info):
    columns_sql = []
    for col in columns_info:
        columns_sql.append(f"{col['name']} {col['mysql_type']}")

    table_creation_query = [
        "id INT AUTO_INCREMENT PRIMARY KEY" # Adiciona ID com autoincremento e sendo chave primária
    ] + columns_sql + [
        "dt_importacao DATETIME DEFAULT CURRENT_TIMESTAMP" # Adiciona data de importação do registro
    ]

    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(table_creation_query)}
    );
    """
    try:
        # cursor atua como intermediário entre o Python e o banco de dados
        cursor.execute(create_table_sql)
        print(f"Tabela '{table_name}' verificada/criada com sucesso.")
    except mysql.connector.Error as error:
        print(f"Erro ao criar/verificar tabela '{table_name}': {error}")


# --- Função para popular tabelas com base nos arquivos lidos ---
def import_fixed_width_file(filepath, conn, table_name, columns_info):
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


def main():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Iteração sobre os arquivos mapeados
            for data_filename, config in FILE_MAPPING.items():
                data_filepath = os.path.join(DADOS_FOLDER, data_filename)
                layout_filepath = os.path.join(DADOS_FOLDER, config['layout_file'])
                table_name = config['table_name']

                # Verifique se ambos os arquivos (layout e dados) existem antes de tentar processar
                if not os.path.exists(layout_filepath):
                    print(f"Aviso: Arquivo de layout '{layout_filepath}' não encontrado. Pulando '{data_filename}'.")
                    continue
                if not os.path.exists(data_filepath):
                    print(f"Aviso: Arquivo de dados '{data_filepath}' não encontrado. Pulando '{data_filename}'.")
                    continue

                columns_info = parse_layout_file(layout_filepath)
                if columns_info:
                    # CREATE_TABLE
                    create_table_from_layout(cursor, table_name, columns_info)
                    conn.commit()
                    # INSERT_INTO
                    import_fixed_width_file(data_filepath, conn, table_name, columns_info)
                else:
                    print(f"Pulando processamento para '{data_filename}' devido a erro na análise do layout ou layout vazio.")
            
            print("\nImportação de todas as tabelas SIGTAP configuradas concluída.")

        except Exception as e:
            conn.rollback()
            print(f"Ocorreu um erro geral durante a importação: {e}")
        finally:
            conn.close()
            print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    main()
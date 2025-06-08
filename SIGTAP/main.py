# Esse código lê dados do SIGTAP e armazena o resultado em uma tabela de banco de dados,
# utilizando arquivos de layout para modelar essas tabelas.

import os
from utils.get_db_connection import get_db_connection
from utils.read_layout_file import read_layout_file
from utils.create_table_from_layout import create_table_from_layout
from utils.import_data import import_data

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

                columns_info = read_layout_file(layout_filepath)
                if columns_info:
                    # CREATE_TABLE
                    create_table_from_layout(cursor, table_name, columns_info)
                    conn.commit()
                    # INSERT_INTO
                    import_data(data_filepath, conn, table_name, columns_info)
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
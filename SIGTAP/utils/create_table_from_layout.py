import mysql.connector
from datetime import datetime

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
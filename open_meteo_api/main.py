import mysql.connector # Importa o conector MySQL
from get_pressure_forecast import get_pressure_forecast_data
from datetime import datetime # Importa o módulo datetime para formatação de data/hora

# Configuração do banco de dados MySQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'open_meteo',
    'user': 'joaosantos',
    'password': '123'
}

def setup_database():
    """
    Conecta-se ao banco de dados MySQL e cria a tabela
    'previsao_pressao_atm' se ela não existir.

    Returns:
        mysql.connector.connection.MySQLConnection: O objeto de conexão com o banco de dados.
    """
    conn = None
    try:
        # Conecta-se ao servidor MySQL
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Cria a tabela previsao_pressao_atm se ela não existir
        # Usando AUTO_INCREMENT para o ID e DATETIME para o momento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS previsao_pressao_atm (
                id INT AUTO_INCREMENT PRIMARY KEY,
                momento DATETIME NOT NULL,
                valor FLOAT NOT NULL
            )
        ''')
        conn.commit()
        print(f"Banco de dados '{DB_CONFIG['database']}' e tabela 'previsao_pressao_atm' configurados com sucesso.")
        return conn
    except mysql.connector.Error as e:
        print(f"Erro ao configurar o banco de dados MySQL: {e}")
        if conn:
            conn.close() # Garante que a conexão seja fechada em caso de erro
        return None

def insert_forecast_data(conn, data):
    """
    Insere os dados da previsão de pressão atmosférica na tabela.

    Args:
        conn (mysql.connector.connection.MySQLConnection): O objeto de conexão com o banco de dados.
        data (list): Uma lista de dicionários com 'momento' e 'valor'.
    """
    if not conn:
        print("Conexão com o banco de dados não estabelecida.")
        return

    cursor = conn.cursor()
    try:
        # Loop pelos dados e insere cada registro na tabela
        sql = "INSERT INTO previsao_pressao_atm (momento, valor) VALUES (%s, %s)"
        
        data_to_insert = []
        for entry in data:
            # Converte a string ISO 8601 (ex: '2025-06-06T13:00:00+00:00') para um objeto datetime
            dt_object = datetime.fromisoformat(entry['momento'].replace('Z', '+00:00'))
            
            # Formata o objeto datetime para a string 'YYYY-MM-DD HH:MM:SS' para inserção no MySQL
            formatted_momento_for_db = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            data_to_insert.append((formatted_momento_for_db, entry['valor']))

        cursor.executemany(sql, data_to_insert)
        conn.commit()
        print(f"Dados inseridos com sucesso na tabela 'previsao_pressao_atm'. Total de {len(data)} registros.")
    except mysql.connector.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
        conn.rollback() # Reverte a transação em caso de erro

def fetch_and_store_pressure_data():
    """
    Orquestra o processo de buscar dados da API e armazená-los no banco de dados.
    """
    print("Iniciando o processo de busca e armazenamento de dados de pressão...")

    # 1. Configura o banco de dados MySQL
    conn = setup_database()
    if not conn:
        print("Não foi possível conectar ao banco de dados. Encerrando.")
        return

    # 2. Busca os dados da previsão da API
    print("Buscando dados da API Open-Meteo...")
    forecast_data = get_pressure_forecast_data()

    if forecast_data:
        # 3. Insere os dados no banco de dados
        print("Inserindo dados no banco de dados...")
        insert_forecast_data(conn, forecast_data)
        print("Processo concluído.")
    else:
        print("Nenhum dado de previsão foi obtido da API. Nenhuma inserção no banco de dados.")

    # 4. Fecha a conexão com o banco de dados
    if conn:
        conn.close()
        print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    fetch_and_store_pressure_data()
    # Para verificar o conteúdo do banco de dados (opcional)
    try:
        conn_check = mysql.connector.connect(**DB_CONFIG)
        cursor_check = conn_check.cursor()
        # Ao selecionar, removemos DATE_FORMAT para exibir o formato armazenado (YYYY-MM-DD HH:MM:SS)
        cursor_check.execute("SELECT id, momento, valor FROM previsao_pressao_atm ORDER BY momento LIMIT 10")
        rows = cursor_check.fetchall()
        print("\nConteúdo do banco de dados (primeiras 10 linhas):")
        for row in rows:
            print(f"ID: {row[0]}, Momento: {row[1]}, Valor: {row[2]} hPa")
        if conn_check:
            conn_check.close()
    except mysql.connector.Error as e:
        print(f"Erro ao verificar o banco de dados MySQL: {e}")


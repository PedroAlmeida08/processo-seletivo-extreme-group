import mysql.connector

# --- Configurações do Banco de Dados MySQL ---
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'stg_prontuario',
    'user': 'joaosantos',
    'password': '123'
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

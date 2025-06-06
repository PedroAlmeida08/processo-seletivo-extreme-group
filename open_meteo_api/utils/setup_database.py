import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'open_meteo',
    'user': 'joaosantos',
    'password': '123'
}

def setup_database():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # CREATE_TABLE
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
            conn.close()
        return None


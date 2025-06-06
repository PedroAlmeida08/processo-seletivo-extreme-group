import mysql.connector
from datetime import datetime

def insert_forecast_data(conn, data):
    
    if not conn:
        print("Conexão com o banco de dados não estabelecida.")
        return

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO previsao_pressao_atm (momento, valor) VALUES (%s, %s)"
        data_to_insert = []
        for entrada in data:
            # Converte tipo de momento para datetime (formato Python)
            momento = datetime.fromisoformat(entrada['momento'].replace('Z', '+00:00'))
            # Converte tipo de momento para DATETIME (formato SQL)
            momento = momento.strftime('%Y-%m-%d %H:%M:%S')
            
            data_to_insert.append((momento, entrada['valor']))

        # executemany para execução em lotes
        cursor.executemany(sql, data_to_insert)
        conn.commit()
        print(f"Dados inseridos com sucesso na tabela 'previsao_pressao_atm'. Total de {len(data)} registros.")
    except mysql.connector.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
        conn.rollback() # Reverte a transação em caso de erro


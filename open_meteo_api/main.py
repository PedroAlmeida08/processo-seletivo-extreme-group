from utils.setup_database import setup_database
from utils.get_pressure_forecast import get_pressure_forecast_data
from utils.insert_forecast_data import insert_forecast_data

def main():
    # 1. Conecta ao banco de dados
    conn = setup_database()
    if not conn:
        print("Não foi possível conectar ao banco de dados.")
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
    main()

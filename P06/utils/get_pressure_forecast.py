import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

def get_pressure_forecast_data():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -22.9068,
        "longitude": -43.1729,
        "hourly": "surface_pressure",
        "timezone": "America/Sao_Paulo"
        # Não é necessário pois 7 é o valor padrão para forecast_days
        # "forecast_days": 7
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
    
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_surface_pressure = hourly.Variables(0).ValuesAsNumpy()

        # Create Pandas DataFrame
        hourly_data = {
            "date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            ),
            "surface_pressure": hourly_surface_pressure
        }

        hourly_dataframe = pd.DataFrame(data = hourly_data)

        # Converte o DataFrame para uma lista de dicionários no formato desejado para o banco de dados
        # Cada dicionário terá as chaves 'momento' (timestamp) e 'valor' (float)
        # O 'momento' é convertido para o formato ISO para fácil inserção no SQLite
        forecast_list = []
        for index, row in hourly_dataframe.iterrows():
            forecast_list.append({
                "momento": row["date"].isoformat(),
                "valor": float(row["surface_pressure"])
            })
        
        return forecast_list

    except Exception as e:
        print(f"Erro ao buscar dados da API Open-Meteo: {e}")
        return []
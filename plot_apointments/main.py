import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_appointments_per_day(dates, filename = 'atendimentos_por_dia.png', folder = 'plots'):
    
    if not dates:
        return "A lista de datas está vazia. Nenhuma visualização pode ser gerada."

    # Converte a lista em uma Series do Pandas, onde cada elemento é uma string de data.
    appointments_series = pd.to_datetime(pd.Series(dates))
    # Converte cada string em objetos datetime do Python
    appointments_per_day = appointments_series.value_counts().sort_index()

    plt.figure(figsize=(14, 7))
    graph = appointments_per_day.plot(kind='bar', color='skyblue', width=0.5)

    x_positions = range(len(appointments_per_day)) 

    graph.plot(
        x_positions,
        appointments_per_day.values,
        color='navy',
        marker='o',
        linewidth=2
    )
    
    for i, count in enumerate(appointments_per_day):
        graph.text(
            x = i,              
            y = count,          
            s = str(count),     
            ha = 'center',      
            va = 'bottom',      
            fontsize = 14,
            color = 'black'
        )

    plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.title('Número de Atendimentos Médicos por Dia', fontsize=16)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Número de Atendimentos', fontsize=12)
    plt.tight_layout()
    
    output_path = os.path.join(os.path.dirname(__file__), folder)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    full_path = os.path.join(output_path, filename)

    try:
        plt.savefig(full_path)
        plt.close()
        return f"Gráfico salvo com sucesso em: {full_path}"
    except Exception as e:
        plt.close()
        return f"Erro ao salvar o gráfico: {e}"

# --- Exemplos ---

exemplo_1 = [
    "2025-05-26",
    "2025-05-27", "2025-05-27",
    "2025-05-28", "2025-05-28", "2025-05-28",
    "2025-05-29", "2025-05-29",
    "2025-05-30",
    "2025-05-31"
]
print(plot_appointments_per_day(
        exemplo_1,
        filename='atendimentos_maio.png'
))

exemplo_2 = [
    "2025-06-01",
    "2025-06-02", "2025-06-02",
    "2025-06-03", "2025-06-03", "2025-06-03",
    "2025-06-04", "2025-06-04", "2025-06-04", "2025-06-04", "2025-06-04",
    "2025-06-05", "2025-06-05",
    "2025-06-06"
]
print(plot_appointments_per_day(
        exemplo_2,
        filename='atendimentos_junho.png'
))

exemplo_3 = [
    "2025-06-01", "2025-06-01",
    "2025-06-02", "2025-06-02", "2025-06-02",
    "2025-06-03",
    "2025-06-04",
    "2025-06-06", "2025-06-06"
]
print(plot_appointments_per_day(
        exemplo_3,
        filename='atendimentos_julho.png'
))
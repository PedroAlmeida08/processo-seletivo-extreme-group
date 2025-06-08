from utils.plot_apointments_per_day import plot_appointments_per_day

if __name__ == "__main__":
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
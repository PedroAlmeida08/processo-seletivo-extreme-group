from contar_prescricoes import contar_prescricoes

def verifica_prescricao(prescricao: str, estoque: str):
    
    ct_prescricao = contar_prescricoes(prescricao)
    ct_estoque = contar_prescricoes(estoque)

    # .items() é utilizado em dicionários para retornar o par (chave, valor)
    for medicamento, qtd_prescrita in ct_prescricao.items():
        if ct_estoque.get(medicamento, 0) < qtd_prescrita:
            return "false"
    
    return "true"
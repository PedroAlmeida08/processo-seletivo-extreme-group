def contar_frequencias(texto: str):
        frequencias = {}
        for char in texto:
            # .get(char, 0) retorna o valor contido na chave "char" se a encontrar
            # no dicionário, caso contrário, retorna o valor definido como padrão
            # nesse caso, 0.
            frequencias[char] = frequencias.get(char, 0) + 1
        return frequencias


def verifica_prescricao(prescricao: str, estoque: str):
    
    ct_prescricao = contar_frequencias(prescricao)
    ct_estoque = contar_frequencias(estoque)

    # .items() é utilizado em dicionários para retornar o par (chave, valor)
    for medicamento, qtd_prescrita in ct_prescricao.items():
        if ct_estoque.get(medicamento, 0) < qtd_prescrita:
            return "false"
    
    return "true"


if __name__ == "__main__":
    print(verifica_prescricao('a', 'b'))
    print(verifica_prescricao('aa', 'b'))
    print(verifica_prescricao('aa', 'aab')) 
    print(verifica_prescricao('aba', 'cbaa'))